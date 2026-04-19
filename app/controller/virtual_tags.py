"""
Anomalies controller.
"""

from typing import Any, List
from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas

virtual_tags_controller = APIRouter(prefix="/virtual-tags", tags=["Virtual Tags"])



@virtual_tags_controller.get("/sample")
def sample_virtual_tags():
    return {
        'data':[],
        'msg': "Virtual tags fetched successfully"
    }


