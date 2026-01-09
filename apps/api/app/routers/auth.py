from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.models import User
from app.schemas.auth import OtpRequest, OtpVerify, TokenResponse
from app.services.otp import otp_store

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/request")
def request_otp(payload: OtpRequest) -> dict:
    otp = otp_store.create(payload.phone)
    return {"message": "OTP sent", "dev_otp": otp}


@router.post("/otp/verify", response_model=TokenResponse)
def verify_otp(payload: OtpVerify, db: Session = Depends(get_db)) -> TokenResponse:
    if not otp_store.verify(payload.phone, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    try:
        role = UserRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid role") from exc

    user = db.query(User).filter(User.phone == payload.phone).first()
    if not user:
        user = User(phone=payload.phone, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token({"sub": user.id, "role": user.role.value})
    return TokenResponse(access_token=token)
