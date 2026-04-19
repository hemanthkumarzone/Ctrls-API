"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

reports_controller = APIRouter(prefix="/reports", tags=["Reports"])



@reports_controller.get("/sample")
def sample_reports():
    return {
        'data':[],
        'msg': "Reports fetched successfully"
    }


