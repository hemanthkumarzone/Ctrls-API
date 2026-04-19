"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

dashboard_controller = APIRouter(prefix="/dashboard", tags=["Dashboard"])



@dashboard_controller.get("/sample")
def sample_dashboard():
    return {
        'data':[],
        'msg': "Dashboard data fetched successfully"
    }


