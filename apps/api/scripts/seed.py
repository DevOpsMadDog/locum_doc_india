from datetime import datetime, timedelta
import random

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.enums import ShiftStatus, Specialty, UserRole
from app.models.models import ClinicProfile, DoctorProfile, Shift, User

clinic_names = [
    "Sunrise Dental",
    "Marina Health",
    "Velachery Dental",
]


def seed() -> None:
    db: Session = SessionLocal()
    clinics = []
    for i, name in enumerate(clinic_names):
        user = User(
            role=UserRole.clinic_admin,
            phone=f"+9199000001{i}",
            email=f"clinic{i}@locum.test",
            hashed_auth=hash_password("password"),
        )
        db.add(user)
        db.flush()
        clinic = ClinicProfile(
            user_id=user.id,
            name=name,
            address="Chennai",
            lat=13.05 + i * 0.01,
            lng=80.24 + i * 0.01,
            city="Chennai",
        )
        db.add(clinic)
        clinics.append(clinic)

    doctors = []
    specialties = list(Specialty)
    for i in range(20):
        user = User(
            role=UserRole.doctor,
            phone=f"+919900010{i:02d}",
            email=f"doctor{i}@locum.test",
            hashed_auth=hash_password("password"),
        )
        db.add(user)
        db.flush()
        doctor = DoctorProfile(
            user_id=user.id,
            full_name=f"Dr. Demo {i}",
            specialty=random.choice(specialties),
            reg_no=f"TN{i:05d}",
        )
        db.add(doctor)
        doctors.append(doctor)

    db.flush()
    for i in range(30):
        clinic = random.choice(clinics)
        start = datetime.utcnow() + timedelta(days=random.randint(0, 5), hours=9)
        shift = Shift(
            clinic_id=clinic.id,
            specialty=random.choice(specialties),
            start_time=start,
            end_time=start + timedelta(hours=4),
            pay_amount=random.choice([3500, 4000, 4500, 5000]),
            address="Chennai",
            lat=clinic.lat,
            lng=clinic.lng,
            notes="Demo shift",
            status=ShiftStatus.posted,
        )
        db.add(shift)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
