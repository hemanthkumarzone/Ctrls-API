"""
Cost and billing endpoints.
"""

from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models import User
from app.services.cost_service import CostService

router = APIRouter()
cost_service = CostService()


@router.get("/overview", response_model=schemas.CostOverview)
def get_cost_overview(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get cost overview for tenant."""
    overview = cost_service.get_cost_overview(
        db, start_date=start_date, end_date=end_date
    )
    return overview


@router.get("/by-service", response_model=List[schemas.CostByService])
def get_cost_by_service(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get cost breakdown by service."""
    costs = cost_service.get_cost_by_service(
        db, start_date=start_date, end_date=end_date
    )
    return costs


@router.get("/by-job", response_model=List[schemas.CostByJob])
def get_cost_by_job(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    limit: int = 50,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get cost breakdown by job."""
    costs = cost_service.get_cost_by_job(
        db, start_date=start_date, end_date=end_date, limit=limit
    )
    return costs


@router.get("/anomalies", response_model=List[schemas.CostAnomaly])
def get_cost_anomalies(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    threshold: float = 2.0,  # z-score threshold
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get cost anomalies using statistical analysis."""
    anomalies = cost_service.detect_anomalies(
        db, start_date=start_date, end_date=end_date, threshold=threshold
    )
    return anomalies


@router.get("/trend", response_model=List[schemas.CostTrend])
def get_cost_trend(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    granularity: str = "day",  # day, week, month
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get cost trend over time."""
    trend = cost_service.get_cost_trend(
        db, start_date=start_date, end_date=end_date, granularity=granularity
    )
    return trend


@router.get("/idle-cost", response_model=schemas.IdleCostSummary)
def get_idle_cost_summary(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    utilization_threshold: float = 0.1,  # 10% utilization threshold
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get summary of idle resource costs."""
    summary = cost_service.get_idle_cost_summary(
        db, start_date=start_date, end_date=end_date,
        utilization_threshold=utilization_threshold
    )
    return summary


@router.get("/top-expensive-jobs", response_model=List[schemas.JobCostAggregate])
def get_top_expensive_jobs(
    db: Session = Depends(deps.get_db_with_tenant),
    start_date: datetime = None,
    end_date: datetime = None,
    limit: int = 10,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get top expensive jobs."""
    jobs = cost_service.get_top_expensive_jobs(
        db, start_date=start_date, end_date=end_date, limit=limit
    )
    return jobs