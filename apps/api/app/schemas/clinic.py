from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import ShiftStatus, Specialty


class ClinicProfileCreate(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    city: str = "Chennai"
    pan: Optional[str] = None
    gst: Optional[str] = None


class ClinicProfileOut(BaseModel):
    id: int
    name: str
    address: str
    lat: float
    lng: float
    city: str

    class Config:
        from_attributes = True


class ShiftCreate(BaseModel):
    specialty: Specialty
    start_time: datetime
    end_time: datetime
    pay_amount: float
    address: str
    lat: float
    lng: float
    notes: Optional[str] = None
    auto_replace: bool = False


class ShiftOut(BaseModel):
    id: int
    specialty: Specialty
    start_time: datetime
    end_time: datetime
    pay_amount: float
    address: str
    lat: float
    lng: float
    notes: Optional[str]
    status: ShiftStatus

    class Config:
        from_attributes = True
