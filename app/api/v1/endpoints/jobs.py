"""
Orchestration job management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models import User
from app.services.job_service import JobService

router = APIRouter()
job_service = JobService()


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
    db: Session = Depends(deps.get_db_with_tenant),
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    agent_id: str = None,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve jobs with optional filters."""
    jobs = job_service.get_jobs(
        db,
        skip=skip,
        limit=limit,
        status=status_filter,
        agent_id=agent_id,
    )
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_in: schemas.JobCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Create new job."""
    job = job_service.create_job(db, job_in)
    return job


@router.get("/{job_id}", response_model=schemas.Job)
def read_job(
    *,
    job_id: str,
    db: Session = Depends(deps.get_db_with_tenant),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get job by ID."""
    job = job_service.get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


@router.put("/{job_id}", response_model=schemas.Job)
def update_job(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    job_in: schemas.JobUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Update job."""
    job = job_service.update_job(db, job_id=job_id, job_in=job_in)
    return job


@router.delete("/{job_id}")
def delete_job(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Delete job."""
    job_service.delete_job(db, job_id=job_id)
    return {"message": "Job deleted successfully"}


@router.post("/{job_id}/start", response_model=schemas.Job)
def start_job(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Start a job."""
    job = job_service.start_job(db, job_id=job_id)
    return job


@router.post("/{job_id}/stop", response_model=schemas.Job)
def stop_job(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Stop a job."""
    job = job_service.stop_job(db, job_id=job_id)
    return job


@router.get("/{job_id}/cost", response_model=schemas.JobCostAggregate)
def get_job_cost(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get job cost aggregate."""
    cost_aggregate = job_service.get_job_cost_aggregate(db, job_id=job_id)
    if not cost_aggregate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost aggregate not found",
        )
    return cost_aggregate


@router.post("/{job_id}/cost/aggregate")
def aggregate_job_cost(
    *,
    db: Session = Depends(deps.get_db_with_tenant),
    job_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Trigger cost aggregation for job."""
    job_service.aggregate_job_cost(db, job_id=job_id)
    return {"message": "Cost aggregation triggered"}