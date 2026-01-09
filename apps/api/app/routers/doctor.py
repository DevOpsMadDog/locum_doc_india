from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import AssignmentStatus, ShiftStatus, UserRole
from app.models.models import DoctorProfile, Shift, ShiftAssignment, ShiftEvent, LocationPing
from app.schemas.assignment import AssignmentStatusUpdate, LocationPingCreate
from app.schemas.doctor import DoctorProfileCreate, DoctorProfileOut
from app.services.realtime import manager
from app.services.status_machine import can_transition_assignment, can_transition_shift

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/me", response_model=DoctorProfileOut)
def create_doctor_profile(
    payload: DoctorProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> DoctorProfileOut:
    if user.role != UserRole.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = db.query(DoctorProfile).filter(DoctorProfile.user_id == user.id).first()
    if profile:
        raise HTTPException(status_code=400, detail="Doctor profile exists")
    profile = DoctorProfile(user_id=user.id, **payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me", response_model=DoctorProfileOut)
def get_doctor_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> DoctorProfileOut:
    profile = db.query(DoctorProfile).filter(DoctorProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return profile


@router.get("/jobs/available")
def list_available_jobs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> list[dict]:
    if user.role != UserRole.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")
    shifts = db.query(Shift).filter(Shift.status == ShiftStatus.posted).all()
    return [
        {
            "id": shift.id,
            "specialty": shift.specialty.value,
            "start_time": shift.start_time,
            "end_time": shift.end_time,
            "pay_amount": float(shift.pay_amount),
            "address": shift.address,
            "lat": shift.lat,
            "lng": shift.lng,
        }
        for shift in shifts
    ]


@router.post("/assignments/{assignment_id}/accept")
def accept_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    if user.role != UserRole.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")
    assignment = db.get(ShiftAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not can_transition_assignment(assignment.status, AssignmentStatus.accepted):
        raise HTTPException(status_code=400, detail="Assignment not in acceptable state")
    assignment.status = AssignmentStatus.accepted
    assignment.accepted_at = datetime.utcnow()
    db.add(ShiftEvent(shift_id=assignment.shift_id, assignment_id=assignment.id, event="accepted"))
    db.commit()
    return {"status": assignment.status.value}


@router.post("/assignments/{assignment_id}/status")
async def update_assignment_status(
    assignment_id: int,
    payload: AssignmentStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    if user.role != UserRole.doctor:
        raise HTTPException(status_code=403, detail="Not authorized")
    assignment = db.get(ShiftAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not can_transition_assignment(assignment.status, payload.status):
        raise HTTPException(status_code=400, detail="Invalid assignment transition")
    assignment.status = payload.status
    event_map = {
        AssignmentStatus.en_route: "en_route",
        AssignmentStatus.checked_in: "checked_in",
        AssignmentStatus.completed: "completed",
    }
    if payload.status in event_map:
        db.add(ShiftEvent(shift_id=assignment.shift_id, assignment_id=assignment.id, event=event_map[payload.status]))
    shift = db.get(Shift, assignment.shift_id)
    if shift:
        next_shift_status = {
            AssignmentStatus.en_route: ShiftStatus.en_route,
            AssignmentStatus.checked_in: ShiftStatus.checked_in,
            AssignmentStatus.completed: ShiftStatus.completed,
        }.get(payload.status)
        if next_shift_status and can_transition_shift(shift.status, next_shift_status):
            shift.status = next_shift_status
    db.commit()
    await manager.broadcast(
        f"assignment:{assignment_id}",
        {"type": "status_update", "status": assignment.status.value},
    )
    return {"status": assignment.status.value}


@router.post("/assignments/{assignment_id}/location")
async def create_location_ping(
    assignment_id: int,
    payload: LocationPingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    assignment = db.get(ShiftAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    shift = db.get(Shift, assignment.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    tracking_start = shift.start_time - timedelta(minutes=30)
    tracking_end = shift.end_time
    now = datetime.utcnow()
    if not (tracking_start <= now <= tracking_end):
        raise HTTPException(status_code=400, detail="Tracking not allowed outside duty window")
    ping = LocationPing(assignment_id=assignment_id, **payload.model_dump())
    db.add(ping)
    db.commit()
    await manager.broadcast(
        f"assignment:{assignment_id}",
        {"type": "location_ping", "lat": payload.lat, "lng": payload.lng},
    )
    return {"status": "ok"}
