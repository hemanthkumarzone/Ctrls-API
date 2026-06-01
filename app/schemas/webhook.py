from pydantic import BaseModel


class RazorpayWebhookPayload(BaseModel):
    event: str