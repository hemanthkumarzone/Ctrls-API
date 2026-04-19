"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

anomalies_controller = APIRouter(prefix="/anomalies", tags=["Anomalies"])



@anomalies_controller.get("/sample")
def sample_anomalies():
    return {
        'data':[],
        'msg': "Anomalies fetched successfully"
    }


