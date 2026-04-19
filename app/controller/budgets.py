"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

budgets_controller = APIRouter(prefix="/budgets", tags=["Budgets"])



@budgets_controller.get("/sample")
def sample_budgets():
    return {
        'data':[],
        'msg': "Budgets fetched successfully"
    }


