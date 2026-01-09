from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    shift_id: int
    amount: float


class CreateOrderResponse(BaseModel):
    order_id: str
    amount: float
    currency: str = "INR"


class PayoutRequest(BaseModel):
    shift_id: int
    doctor_id: int
    amount: float


class PayoutResponse(BaseModel):
    payout_id: str
    status: str
