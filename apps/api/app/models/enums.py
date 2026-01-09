import enum


class UserRole(str, enum.Enum):
    clinic_admin = "clinic_admin"
    clinic_staff = "clinic_staff"
    doctor = "doctor"
    admin = "admin"


class Specialty(str, enum.Enum):
    dentist_general = "dentist_general"
    endodontist = "endodontist"
    anesthetist = "anesthetist"


class VerificationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ShiftStatus(str, enum.Enum):
    draft = "draft"
    posted = "posted"
    booked = "booked"
    en_route = "en_route"
    checked_in = "checked_in"
    completed = "completed"
    paid = "paid"
    canceled = "canceled"
    no_show = "no_show"


class AssignmentStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    canceled = "canceled"
    en_route = "en_route"
    checked_in = "checked_in"
    completed = "completed"


class OtpType(str, enum.Enum):
    checkin = "checkin"
    checkout = "checkout"


class PaymentStatus(str, enum.Enum):
    created = "created"
    paid = "paid"
    failed = "failed"


class PayoutStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
