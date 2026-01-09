import random
from datetime import datetime, timedelta


class OtpStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, datetime]] = {}

    def create(self, phone: str) -> str:
        otp = "".join(str(random.randint(0, 9)) for _ in range(6))
        self._store[phone] = (otp, datetime.utcnow() + timedelta(minutes=5))
        return otp

    def verify(self, phone: str, otp: str) -> bool:
        entry = self._store.get(phone)
        if not entry:
            return False
        code, expires_at = entry
        if datetime.utcnow() > expires_at:
            return False
        return code == otp


otp_store = OtpStore()
