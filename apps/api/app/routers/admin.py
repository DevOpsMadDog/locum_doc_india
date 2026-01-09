from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import UserRole, VerificationStatus
from app.models.models import DoctorProfile

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/doctors/{doctor_id}/verify")
def verify_doctor(
    doctor_id: int,
    status: VerificationStatus,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> dict:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    doctor = db.get(DoctorProfile, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor.verification_status = status
    db.commit()
    return {"status": doctor.verification_status.value}
