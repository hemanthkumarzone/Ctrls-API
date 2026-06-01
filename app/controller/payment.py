from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException
)
from sqlalchemy.orm import Session
from app import schemas
import razorpay
import os
from dotenv import load_dotenv

from app.api.deps import (
    get_db,
    get_current_active_user
)

from app.services.payment_service import payment_service
from app.services.subscription_service import subscription_service
from app.core.config import settings
from app.schemas.payment import (
    PaymentVerificationRequest
)

from app.repositories.payment_repo import (
    payment_repo
)

from app.repositories.subscription_repo import (
    subscription_repo
)
from app.services.payment_receipt_service import (
    payment_receipt_service
)

load_dotenv()

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)



@router.post("/create-order")
async def create_order(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
    get_current_active_user
    )
):
    subscription = subscription_repo.get_by_tenant(
        db,
        current_user.tenant_id
    )

    if not subscription:

        subscription = (
            subscription_service
            .create_trial_subscription(
                db=db,
                tenant_id=current_user.tenant_id,
                plan_name="platform"
            )
        )
    order_data = {
        "amount": 49900,
        "currency": "INR",
        "receipt": "receipt_001",
        "payment_capture": 1
    }

    try:

        order = razorpay_client.order.create(
            data=order_data
        )

    except Exception as e:

        print("================================")
        print("RAZORPAY ERROR =", str(e))
        print("================================")

        raise

    payment_service.create_payment(
        db=db,
        tenant_id=current_user.tenant_id,
        subscription_id=subscription.id,
        amount=499,
        order_id=order["id"]
    )

    return {
        "success": True,
        "order": order
    }

    

@router.post("/verify")
async def verify_payment(
    payload: PaymentVerificationRequest,
    db: Session = Depends(get_db)
):

    try:

        razorpay_client.utility.verify_payment_signature(
            {
                "razorpay_order_id":
                    payload.razorpay_order_id,

                "razorpay_payment_id":
                    payload.razorpay_payment_id,

                "razorpay_signature":
                    payload.razorpay_signature,
            }
        )

        payment = payment_repo.get_by_order_id(
            db,
            payload.razorpay_order_id
        )

        if not payment:
            return {
                "success": False,
                "message": "Payment not found"
            }
        if payment.payment_status == "success":
            return {
                "success": True,
                "message": "Payment already processed"
            }
        
        payment_service.mark_payment_success(
            db=db,
            payment=payment,
            razorpay_payment_id=
                payload.razorpay_payment_id,
            razorpay_signature=
                payload.razorpay_signature,
        )
        payment_receipt_service.create_receipt(
            db=db,
            tenant_id=payment.tenant_id,
            amount=payment.amount,
            payment_id=payload.razorpay_payment_id
        )

        subscription = subscription_repo.get_by_tenant(
            db,
            payment.tenant_id
        )

        if subscription:
            subscription_service.activate_subscription(
                db=db,
                subscription=subscription
            )

        return {
            "success": True,
            "message": "Payment verified successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    body = await request.body()

    signature = request.headers.get(
        "X-Razorpay-Signature"
    )

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing webhook signature"
        )

    try:

        razorpay_client.utility.verify_webhook_signature(
            body.decode(),
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid webhook signature"
        )

    payload = await request.json()

    event = payload.get("event")

    print("WEBHOOK EVENT =", event)

    if event == "payment.captured":

        payment_entity = (
            payload.get("payload", {})
            .get("payment", {})
            .get("entity", {})
        )

        order_id = payment_entity.get("order_id")

        payment = payment_repo.get_by_order_id(
            db,
            order_id
        )

        if payment:

            payment.payment_status = "success"

            db.add(payment)

            db.commit()

    return {
        "success": True
    } 