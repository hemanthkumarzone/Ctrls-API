"""
Job service.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import JobCostAggregate, JobStatus, OrchestrationJob
from app.repositories.job_repo import job_repo
from app.schemas.job import JobCreate, JobUpdate
from app.services.cost_service import CostService


class JobService:
    """Job service."""

    def __init__(self):
        self.cost_service = CostService()

    def get_jobs(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> List[OrchestrationJob]:
        """Get jobs with filters."""
        return job_repo.get_with_filters(
            db, skip=skip, limit=limit, status=status, agent_id=agent_id
        )

    def get_job(self, db: Session, job_id: str) -> Optional[OrchestrationJob]:
        """Get job by ID."""
        return job_repo.get(db, job_id)

    def create_job(self, db: Session, job_in: JobCreate) -> OrchestrationJob:
        """Create new job."""
        job_data = job_in.dict()
        # Set tenant_id from context (would be injected by middleware)
        # job_data["tenant_id"] = get_current_tenant_id()
        return job_repo.create(db, obj_in=job_data)

    def update_job(
        self, db: Session, job_id: str, job_in: JobUpdate
    ) -> OrchestrationJob:
        """Update job."""
        job = self.get_job(db, job_id)
        if not job:
            raise ValueError("Job not found")
        return job_repo.update(db, db_obj=job, obj_in=job_in)

    def delete_job(self, db: Session, job_id: str) -> None:
        """Delete job."""
        job_repo.remove(db, id=job_id)

    def start_job(self, db: Session, job_id: str) -> OrchestrationJob:
        """Start a job."""
        job = self.get_job(db, job_id)
        if not job:
            raise ValueError("Job not found")
        if job.status != JobStatus.QUEUED:
            raise ValueError("Job is not in queued state")

        update_data = JobUpdate(
            status=JobStatus.RUNNING.value,
            started_at=datetime.utcnow()
        )
        return self.update_job(db, job_id, update_data)

    def stop_job(self, db: Session, job_id: str) -> OrchestrationJob:
        """Stop a job."""
        job = self.get_job(db, job_id)
        if not job:
            raise ValueError("Job not found")
        if job.status != JobStatus.RUNNING:
            raise ValueError("Job is not running")

        update_data = JobUpdate(
            status=JobStatus.COMPLETED.value,
            finished_at=datetime.utcnow(),
            duration_seconds=int((datetime.utcnow() - job.started_at).total_seconds())
        )
        return self.update_job(db, job_id, update_data)

    def get_job_cost_aggregate(
        self, db: Session, job_id: str
    ) -> Optional[JobCostAggregate]:
        """Get job cost aggregate."""
        return (
            db.query(JobCostAggregate)
            .filter(JobCostAggregate.job_id == job_id)
            .first()
        )

    def aggregate_job_cost(self, db: Session, job_id: str) -> None:
        """Trigger cost aggregation for job."""
        # This would typically be done asynchronously via Celery
        self.cost_service.aggregate_job_cost(db, job_id)