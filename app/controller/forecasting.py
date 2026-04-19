"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

forecasting_controller = APIRouter(prefix="/forecasting", tags=["Forecasting"])



@forecasting_controller.get("/sample")
def sample_forecasting():
    return {
        'data':[],
        'msg': "Forecasting data fetched successfully"
    }


