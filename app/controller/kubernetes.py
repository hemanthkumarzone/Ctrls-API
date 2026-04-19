"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

kubernetes_controller = APIRouter(prefix="/kubernetes", tags=["Kubernetes"])



@kubernetes_controller.get("/sample")
def sample_kubernetes():
    return {
        'data':[],
        'msg': "Kubernetes data fetched successfully"
    }


