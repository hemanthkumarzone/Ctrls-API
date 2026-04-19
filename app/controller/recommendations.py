"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

recommendations_controller = APIRouter(prefix="/recommendations", tags=["Recommendations"])



@recommendations_controller.get("/sample")
def sample_recommendations():
    return {
        'data':[],
        'msg': "Recommendations fetched successfully"
    }


