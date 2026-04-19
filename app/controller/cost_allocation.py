"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

cost_allocation_controller = APIRouter(prefix="/cost-allocation", tags=["Cost Allocation"])



@cost_allocation_controller.get("/sample")
def sample_cost_allocation():
    return {
        'data':[],
        'msg': "Cost allocation fetched successfully"
    }


