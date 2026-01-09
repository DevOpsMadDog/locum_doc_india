from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import PaymentStatus, PayoutStatus, UserRole
from app.models.models import Payment, Payout, Shift
from app.schemas.payment import CreateOrderRequest, CreateOrderResponse, PayoutRequest, PayoutResponse
from app.services.payments import RazorpayClient

router = APIRouter(prefix="/payments", tags=["payments"])
client = RazorpayClient()


@router.post("/create-order", response_model=CreateOrderResponse)
def create_order(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> CreateOrderResponse:
    if user.role not in {UserRole.clinic_admin, UserRole.clinic_staff}:
        raise HTTPException(status_code=403, detail="Not authorized")
    shift = db.get(Shift, payload.shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    order = client.create_order(payload.amount)
    payment = Payment(
        shift_id=payload.shift_id,
        clinic_id=shift.clinic_id,
        amount=payload.amount,
        provider_order_id=order["id"],
    )
    db.add(payment)
    db.commit()
    return CreateOrderResponse(order_id=order["id"], amount=payload.amount)


@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)) -> dict:
    payload = await request.json()
    order_id = payload.get("order_id")
    payment_id = payload.get("payment_id")
    payment = db.query(Payment).filter(Payment.provider_order_id == order_id).first()
    if payment:
        payment.status = PaymentStatus.paid
        payment.provider_payment_id = payment_id
        db.commit()
    return {"status": "ok"}


@router.post("/payouts/initiate", response_model=PayoutResponse)
def initiate_payout(
    payload: PayoutRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
) -> PayoutResponse:
    if user.role not in {UserRole.admin, UserRole.clinic_admin}:
        raise HTTPException(status_code=403, detail="Not authorized")
    payout_data = client.create_payout(payload.amount)
    payout = Payout(
        shift_id=payload.shift_id,
        doctor_id=payload.doctor_id,
        amount=payload.amount,
        status=PayoutStatus.pending,
        provider_payout_id=payout_data["id"],
    )
    db.add(payout)
    db.commit()
    return PayoutResponse(payout_id=payout_data["id"], status=payout_data["status"])
