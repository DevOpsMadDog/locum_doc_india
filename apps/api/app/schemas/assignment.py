from pydantic import BaseModel

from app.models.enums import AssignmentStatus


class AssignmentStatusUpdate(BaseModel):
    status: AssignmentStatus


class LocationPingCreate(BaseModel):
    lat: float
    lng: float
    speed: float | None = None
    heading: float | None = None
    accuracy: float | None = None
