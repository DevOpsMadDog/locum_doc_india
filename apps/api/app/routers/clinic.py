from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import ShiftStatus, UserRole
from app.models.models import ClinicProfile, Shift, ShiftAssignment, ShiftEvent
from app.schemas.clinic import ClinicProfileCreate, ClinicProfileOut, ShiftCreate, ShiftOut
from app.services.geo import within_service_area
from app.services.status_machine import can_transition_shift

router = APIRouter(prefix="/clinics", tags=["clinics"])


@router.post("/me", response_model=ClinicProfileOut)
def create_clinic_profile(
    payload: ClinicProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ClinicProfileOut:
    if user.role not in {UserRole.clinic_admin, UserRole.clinic_staff}:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not within_service_area(payload.lat, payload.lng):
        raise HTTPException(status_code=400, detail="Location outside Chennai service area")
    profile = db.query(ClinicProfile).filter(ClinicProfile.user_id == user.id).first()
    if profile:
        raise HTTPException(status_code=400, detail="Clinic profile exists")
    profile = ClinicProfile(user_id=user.id, **payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me", response_model=ClinicProfileOut)
def get_clinic_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ClinicProfileOut:
    profile = db.query(ClinicProfile).filter(ClinicProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Clinic profile not found")
    return profile


@router.post("/shifts", response_model=ShiftOut)
def create_shift(
    payload: ShiftCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ShiftOut:
    profile = db.query(ClinicProfile).filter(ClinicProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Clinic profile not found")
    if not within_service_area(payload.lat, payload.lng):
        raise HTTPException(status_code=400, detail="Location outside Chennai service area")
    shift = Shift(
        clinic_id=profile.id,
        status=ShiftStatus.posted,
        **payload.model_dump(),
    )
    db.add(shift)
    db.flush()
    db.add(ShiftEvent(shift_id=shift.id, event="posted"))
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/shifts", response_model=list[ShiftOut])
def list_shifts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> list[ShiftOut]:
    profile = db.query(ClinicProfile).filter(ClinicProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Clinic profile not found")
    return db.query(Shift).filter(Shift.clinic_id == profile.id).all()


@router.get("/shifts/{shift_id}", response_model=ShiftOut)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> ShiftOut:
    shift = db.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@router.get("/shifts/{shift_id}/candidates")
def list_candidates(
    shift_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    shift = db.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    candidates = (
        db.query(ShiftAssignment)
        .filter(ShiftAssignment.shift_id == shift_id)
        .all()
    )
    return {"shift_id": shift_id, "candidates": [c.id for c in candidates]}


@router.post("/shifts/{shift_id}/book")
def book_shift(
    shift_id: int,
    doctor_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    shift = db.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    if not can_transition_shift(shift.status, ShiftStatus.booked):
        raise HTTPException(status_code=400, detail="Shift not in bookable state")
    assignment = ShiftAssignment(shift_id=shift_id, doctor_id=doctor_id)
    shift.status = ShiftStatus.booked
    db.add(assignment)
    db.flush()
    db.add(ShiftEvent(shift_id=shift_id, assignment_id=assignment.id, event="booked"))
    db.commit()
    return {"assignment_id": assignment.id}


@router.get("/assignments/{assignment_id}/live")
def assignment_live(
    assignment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    assignment = db.get(ShiftAssignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    last_ping = (
        assignment.location_pings[-1] if assignment.location_pings else None
    )
    return {
        "assignment_id": assignment.id,
        "status": assignment.status.value,
        "last_ping": {
            "lat": last_ping.lat,
            "lng": last_ping.lng,
            "ts": last_ping.ts,
        }
        if last_ping
        else None,
        "timestamp": datetime.utcnow(),
    }


@router.get("/shifts/{shift_id}/invoice", response_class=HTMLResponse)
def shift_invoice(
    shift_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> str:
    shift = db.get(Shift, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return f\"\"\"\n    <html>\n      <head><title>LocumMap Invoice</title></head>\n      <body style='font-family: Arial, sans-serif;'>\n        <h2>LocumMap Chennai Invoice</h2>\n        <p>Shift ID: {shift.id}</p>\n        <p>Clinic ID: {shift.clinic_id}</p>\n        <p>Specialty: {shift.specialty.value}</p>\n        <p>Pay Amount: ₹{shift.pay_amount}</p>\n        <p>Start: {shift.start_time}</p>\n        <p>End: {shift.end_time}</p>\n        <p>Status: {shift.status.value}</p>\n      </body>\n    </html>\n    \"\"\"\n*** End Patch"}へfunctions.apply_patch to=functions.apply_patch
