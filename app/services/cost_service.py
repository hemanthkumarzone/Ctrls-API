"""
Cost service with FinOps intelligence.
"""

import statistics
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import CostLineItem, JobCostAggregate, JobResourceUsage, OrchestrationJob
from app.repositories.cost_repo import cost_repo
from app.schemas.cost import (
    CostAnomaly,
    CostByJob,
    CostByService,
    CostOverview,
    CostTrend,
    IdleCostSummary,
)


class CostService:
    """Cost service with advanced analytics."""

    def get_cost_overview(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> CostOverview:
        """Get cost overview."""
        # This would use tenant_id from context
        tenant_id = "dummy-tenant-id"  # Would be injected

        result = cost_repo.get_cost_overview(db, tenant_id, start_date, end_date)

        return CostOverview(
            total_cost=result.total_cost or Decimal("0"),
            compute_cost=result.compute_cost or Decimal("0"),
            accelerator_cost=Decimal("0"),  # Would calculate from accelerators
            storage_cost=Decimal("0"),  # Would calculate from storage
            network_cost=Decimal("0"),  # Would calculate from network
            llm_token_cost=Decimal("0"),  # Would calculate from LLM usage
            other_cost=Decimal("0"),
            period_start=start_date or datetime.utcnow() - timedelta(days=30),
            period_end=end_date or datetime.utcnow(),
        )

    def get_cost_by_service(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[CostByService]:
        """Get cost by service."""
        tenant_id = "dummy-tenant-id"
        results = cost_repo.get_cost_by_service(db, tenant_id, start_date, end_date)

        total_cost = sum(r.cost for r in results) if results else Decimal("0")

        return [
            CostByService(
                service=result.service,
                cost=result.cost,
                percentage=(result.cost / total_cost * 100) if total_cost > 0 else Decimal("0")
            )
            for result in results
        ]

    def get_cost_by_job(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[CostByJob]:
        """Get cost by job."""
        tenant_id = "dummy-tenant-id"

        results = (
            db.query(
                JobCostAggregate.job_id,
                OrchestrationJob.name.label("job_name"),
                JobCostAggregate.total_cost_usd.label("cost"),
                OrchestrationJob.duration_seconds,
            )
            .join(OrchestrationJob, JobCostAggregate.job_id == OrchestrationJob.id)
            .filter(JobCostAggregate.tenant_id == tenant_id)
            .order_by(JobCostAggregate.total_cost_usd.desc())
            .limit(limit)
            .all()
        )

        return [
            CostByJob(
                job_id=result.job_id,
                job_name=result.job_name,
                cost=result.cost,
                duration_seconds=result.duration_seconds,
            )
            for result in results
        ]

    def detect_anomalies(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        threshold: float = 2.0,
    ) -> List[CostAnomaly]:
        """Detect cost anomalies using z-score."""
        tenant_id = "dummy-tenant-id"

        # Get daily costs for the period
        daily_costs = (
            db.query(
                func.date(CostLineItem.usage_start).label("date"),
                func.sum(CostLineItem.cost_usd).label("cost")
            )
            .filter(CostLineItem.tenant_id == tenant_id)
            .filter(CostLineItem.usage_start >= start_date) if start_date else db.query()
            .filter(CostLineItem.usage_end <= end_date) if end_date else db.query()
            .group_by(func.date(CostLineItem.usage_start))
            .order_by(func.date(CostLineItem.usage_start))
            .all()
        )

        if len(daily_costs) < 7:  # Need at least a week of data
            return []

        costs = [float(dc.cost) for dc in daily_costs]
        mean = statistics.mean(costs)
        stdev = statistics.stdev(costs)

        anomalies = []
        for dc in daily_costs:
            z_score = (float(dc.cost) - mean) / stdev if stdev > 0 else 0
            if abs(z_score) > threshold:
                severity = "high" if abs(z_score) > 3 else "medium" if abs(z_score) > 2 else "low"
                anomalies.append(
                    CostAnomaly(
                        date=dc.date,
                        expected_cost=Decimal(str(mean)),
                        actual_cost=dc.cost,
                        z_score=Decimal(str(z_score)),
                        severity=severity,
                    )
                )

        return anomalies

    def get_cost_trend(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        granularity: str = "day",
    ) -> List[CostTrend]:
        """Get cost trend over time."""
        tenant_id = "dummy-tenant-id"

        if granularity == "day":
            date_func = func.date(CostLineItem.usage_start)
        elif granularity == "week":
            date_func = func.date_trunc('week', CostLineItem.usage_start)
        elif granularity == "month":
            date_func = func.date_trunc('month', CostLineItem.usage_start)
        else:
            date_func = func.date(CostLineItem.usage_start)

        trend_data = (
            db.query(
                date_func.label("date"),
                func.sum(CostLineItem.cost_usd).label("cost")
            )
            .filter(CostLineItem.tenant_id == tenant_id)
            .filter(CostLineItem.usage_start >= start_date) if start_date else db.query()
            .filter(CostLineItem.usage_end <= end_date) if end_date else db.query()
            .group_by(date_func)
            .order_by(date_func)
            .all()
        )

        trends = []
        prev_cost = None
        for td in trend_data:
            change_percentage = None
            if prev_cost is not None and prev_cost > 0:
                change_percentage = Decimal(str((float(td.cost) - float(prev_cost)) / float(prev_cost) * 100))

            trends.append(
                CostTrend(
                    date=td.date,
                    cost=td.cost,
                    change_percentage=change_percentage,
                )
            )
            prev_cost = td.cost

        return trends

    def get_idle_cost_summary(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        utilization_threshold: float = 0.1,
    ) -> IdleCostSummary:
        """Get idle cost summary."""
        tenant_id = "dummy-tenant-id"

        # Calculate idle costs based on low utilization
        idle_costs = (
            db.query(func.sum(JobResourceUsage.cost_usd))
            .join(OrchestrationJob, JobResourceUsage.job_id == OrchestrationJob.id)
            .filter(OrchestrationJob.tenant_id == tenant_id)
            .filter(JobResourceUsage.avg_utilization_pct < utilization_threshold * 100)
            .filter(OrchestrationJob.started_at >= start_date) if start_date else db.query()
            .filter(OrchestrationJob.finished_at <= end_date) if end_date else db.query()
            .scalar()
        ) or Decimal("0")

        total_cost = (
            db.query(func.sum(JobResourceUsage.cost_usd))
            .join(OrchestrationJob, JobResourceUsage.job_id == OrchestrationJob.id)
            .filter(OrchestrationJob.tenant_id == tenant_id)
            .filter(OrchestrationJob.started_at >= start_date) if start_date else db.query()
            .filter(OrchestrationJob.finished_at <= end_date) if end_date else db.query()
            .scalar()
        ) or Decimal("1")  # Avoid division by zero

        idle_percentage = (idle_costs / total_cost * 100) if total_cost > 0 else Decimal("0")

        return IdleCostSummary(
            total_idle_cost=idle_costs,
            idle_percentage=idle_percentage,
            potential_savings=idle_costs * Decimal("0.8"),  # Assume 80% savings if optimized
        )

    def get_top_expensive_jobs(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
    ) -> List[JobCostAggregate]:
        """Get top expensive jobs."""
        tenant_id = "dummy-tenant-id"
        return cost_repo.get_top_expensive_jobs(db, tenant_id, limit)

    def aggregate_job_cost(self, db: Session, job_id: str) -> None:
        """Aggregate cost for a specific job."""
        # This would calculate costs from various sources and create/update JobCostAggregate
        # For now, just a placeholder
        pass