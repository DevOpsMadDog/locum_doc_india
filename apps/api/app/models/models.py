from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums import (
    AssignmentStatus,
    OtpType,
    PaymentStatus,
    PayoutStatus,
    ShiftStatus,
    Specialty,
    UserRole,
    VerificationStatus,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    hashed_auth = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic_profile = relationship("ClinicProfile", back_populates="user", uselist=False)
    doctor_profile = relationship("DoctorProfile", back_populates="user", uselist=False)


class ClinicProfile(Base):
    __tablename__ = "clinic_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    city = Column(String(64), nullable=False, default="Chennai")
    pan = Column(String(32), nullable=True)
    gst = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="clinic_profile")
    shifts = relationship("Shift", back_populates="clinic")


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    specialty = Column(Enum(Specialty), nullable=False)
    reg_no = Column(String(64), nullable=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.pending)
    home_lat = Column(Float, nullable=True)
    home_lng = Column(Float, nullable=True)
    cancels_count = Column(Integer, default=0)
    no_show_count = Column(Integer, default=0)
    on_time_rate = Column(Float, default=1.0)
    avg_rating = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="doctor_profile")
    credentials = relationship("Credential", back_populates="doctor")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"), nullable=False)
    type = Column(String(64), nullable=False)
    file_url = Column(String(512), nullable=False)
    status = Column(String(32), default="pending")
    expires_at = Column(DateTime, nullable=True)

    doctor = relationship("DoctorProfile", back_populates="credentials")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    clinic_id = Column(Integer, ForeignKey("clinic_profiles.id"), nullable=False)
    specialty = Column(Enum(Specialty), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    pay_amount = Column(Numeric(10, 2), nullable=False)
    address = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    auto_replace = Column(Boolean, default=False)
    status = Column(Enum(ShiftStatus), default=ShiftStatus.draft)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("ClinicProfile", back_populates="shifts")
    assignments = relationship("ShiftAssignment", back_populates="shift")
    payments = relationship("Payment", back_populates="shift")


class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"), nullable=False)
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.pending)
    accepted_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)

    shift = relationship("Shift", back_populates="assignments")
    doctor = relationship("DoctorProfile")
    location_pings = relationship("LocationPing", back_populates="assignment")


class LocationPing(Base):
    __tablename__ = "location_pings"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("shift_assignments.id"), nullable=False)
    ts = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)

    assignment = relationship("ShiftAssignment", back_populates="location_pings")


class OtpSession(Base):
    __tablename__ = "otp_sessions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("shift_assignments.id"), nullable=False)
    type = Column(Enum(OtpType), nullable=False)
    otp_code = Column(String(8), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinic_profiles.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.created)
    provider = Column(String(32), default="razorpay")
    provider_order_id = Column(String(128), nullable=True)
    provider_payment_id = Column(String(128), nullable=True)

    shift = relationship("Shift", back_populates="payments")


class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(PayoutStatus), default=PayoutStatus.pending)
    provider_payout_id = Column(String(128), nullable=True)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinic_profiles.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"), nullable=False)
    stars = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)


class ShiftEvent(Base):
    __tablename__ = "shift_events"

    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("shift_assignments.id"), nullable=True)
    event = Column(String(64), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
