from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    tenant_id: str
    plan_name: str
    billing_cycle: str = "monthly"


class SubscriptionResponse(BaseModel):
    id: str
    tenant_id: str
    plan_name: str

    status: str

    trial_start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None

    auto_renew: bool