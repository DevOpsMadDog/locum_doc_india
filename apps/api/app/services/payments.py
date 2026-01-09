import uuid


class RazorpayClient:
    def create_order(self, amount: float) -> dict:
        return {
            "id": f"order_{uuid.uuid4().hex}",
            "amount": int(amount * 100),
            "currency": "INR",
        }

    def create_payout(self, amount: float) -> dict:
        return {
            "id": f"payout_{uuid.uuid4().hex}",
            "status": "pending",
        }
