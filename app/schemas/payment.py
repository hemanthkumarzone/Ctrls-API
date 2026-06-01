from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    tenant_id: str
    plan_name: str
    amount: Decimal
    currency: str = "INR"


class PaymentResponse(BaseModel):
    id: str
    tenant_id: str
    amount: Decimal
    currency: str
    payment_status: str

    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None


class PaymentVerificationRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str