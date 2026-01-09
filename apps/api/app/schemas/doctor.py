from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import AssignmentStatus, Specialty, VerificationStatus


class DoctorProfileCreate(BaseModel):
    full_name: str
    specialty: Specialty
    reg_no: str
    home_lat: Optional[float] = None
    home_lng: Optional[float] = None


class DoctorProfileOut(BaseModel):
    id: int
    full_name: str
    specialty: Specialty
    reg_no: str
    verification_status: VerificationStatus

    class Config:
        from_attributes = True


class AssignmentOut(BaseModel):
    id: int
    shift_id: int
    doctor_id: int
    status: AssignmentStatus
    accepted_at: Optional[datetime]

    class Config:
        from_attributes = True
