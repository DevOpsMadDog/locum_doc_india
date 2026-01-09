from datetime import datetime, timedelta
import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import AssignmentStatus, OtpType, ShiftStatus, UserRole
from app.models.models import OtpSession, Shift, ShiftAssignment, ShiftEvent
from app.services.geo import is_within_geofence
from app.services.status_machine import can_transition_assignment, can_transition_shift

router = APIRouter(prefix="/assignments", tags=["otp"])


@router.post("/{assignment_id}/otp/create")
def create_otp(
    assignment_id: int,
    type: OtpType,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    if user.role not in {UserRole.clinic_admin, UserRole.clinic_staff}:
        raise HTTPException(status_code=403, detail="Not authorized")
    otp_code = "".join(str(random.randint(0, 9)) for _ in range(4))
    session = OtpSession(
        assignment_id=assignment_id,
        type=type,
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )
    db.add(session)
    db.commit()
    return {"otp": otp_code, "expires_at": session.expires_at}


@router.post("/{assignment_id}/otp/verify")
def verify_otp(
    assignment_id: int,
    type: OtpType,
    otp: str,
    lat: float,
    lng: float,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    assignment = db.get(ShiftAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    shift = db.get(Shift, assignment.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    session = (
        db.query(OtpSession)
        .filter(
            OtpSession.assignment_id == assignment_id,
            OtpSession.type == type,
            OtpSession.used_at.is_(None),
        )
        .order_by(OtpSession.id.desc())
        .first()
    )
    if not session or session.otp_code != otp or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP invalid or expired")

    if not is_within_geofence(lat, lng, shift.lat, shift.lng):
        raise HTTPException(status_code=400, detail="Outside geofence")

    session.used_at = datetime.utcnow()
    if type == OtpType.checkin:
        if not can_transition_assignment(assignment.status, AssignmentStatus.checked_in):
            raise HTTPException(status_code=400, detail="Invalid check-in state")
        assignment.status = AssignmentStatus.checked_in
        if can_transition_shift(shift.status, ShiftStatus.checked_in):
            shift.status = ShiftStatus.checked_in
        db.add(ShiftEvent(shift_id=shift.id, assignment_id=assignment.id, event="checked_in"))
    else:
        if not can_transition_assignment(assignment.status, AssignmentStatus.completed):
            raise HTTPException(status_code=400, detail="Invalid checkout state")
        assignment.status = AssignmentStatus.completed
        if can_transition_shift(shift.status, ShiftStatus.completed):
            shift.status = ShiftStatus.completed
        db.add(ShiftEvent(shift_id=shift.id, assignment_id=assignment.id, event="completed"))

    db.commit()
    return {"status": assignment.status.value}
