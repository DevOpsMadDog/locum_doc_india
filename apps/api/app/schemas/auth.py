from pydantic import BaseModel


class OtpRequest(BaseModel):
    phone: str


class OtpVerify(BaseModel):
    phone: str
    otp: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
