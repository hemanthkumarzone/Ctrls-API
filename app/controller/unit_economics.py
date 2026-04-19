"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

unit_economics_controller = APIRouter(prefix="/unit-economics", tags=["Unit Economics"])



@unit_economics_controller.get("/sample")
def sample_unit_economics():
    return {
        'data':[],
        'msg': "Unit economics data fetched successfully"
    }


