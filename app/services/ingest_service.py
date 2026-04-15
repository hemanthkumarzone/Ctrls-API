"""
Ingest service for metrics and inference events.
"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models import Agent, MetricSample, InferenceRequest
from app.repositories.metrics_repo import metric_repo
from app.repositories.resource_repo import resource_repo
from app.schemas.ingest import MetricBatch, InferenceBatch


class IngestService:
    """Ingest service."""

    def ingest_metrics(
        self,
        db: Session,
        agent: Agent,
        payload: MetricBatch,
    ) -> int:
        samples: list[MetricSample] = []
        captured_at = payload.captured_at or datetime.utcnow()

        for item in payload.samples:
            resource = resource_repo.get_or_create(
                db=db,
                tenant_id=agent.tenant_id,
                provider=item.resource_ref.provider,
                resource_type=item.resource_ref.resource_type,
                external_id=item.resource_ref.external_id,
                name=item.resource_ref.name,
                region=item.resource_ref.region,
                tags=item.resource_ref.tags,
                metadata=item.resource_ref.metadata,
            )

            sample = MetricSample(
                tenant_id=agent.tenant_id,
                resource_id=resource.id,
                agent_id=agent.id,
                metric_name=item.metric_name,
                value=item.value,
                unit=item.unit,
                timestamp=item.timestamp or captured_at,
                dimensions=item.dimensions or {},
                raw={
                    "resource_ref": item.resource_ref.model_dump(),
                },
            )
            samples.append(sample)

        metric_repo.create_samples(db, samples)
        return len(samples)

    def ingest_inference(
        self,
        db: Session,
        agent: Agent,
        payload: InferenceBatch,
    ) -> int:
        requests: list[InferenceRequest] = []
        captured_at = payload.captured_at or datetime.utcnow()

        for event in payload.events:
            if event.resource_ref:
                resource = resource_repo.get_or_create(
                    db=db,
                    tenant_id=agent.tenant_id,
                    provider=event.resource_ref.provider,
                    resource_type=event.resource_ref.resource_type,
                    external_id=event.resource_ref.external_id,
                    name=event.resource_ref.name,
                    region=event.resource_ref.region,
                    tags=event.resource_ref.tags,
                    metadata=event.resource_ref.metadata,
                )
                resource_id = resource.id
            else:
                resource_id = None

            request = InferenceRequest(
                tenant_id=agent.tenant_id,
                resource_id=resource_id,
                agent_id=agent.id,
                model_name=event.model_name,
                request_id=event.request_id,
                status=event.status,
                latency_ms=event.latency_ms,
                input_tokens=event.input_tokens,
                output_tokens=event.output_tokens,
                gpu_ms=event.gpu_ms,
                cost_usd=event.cost_usd or Decimal("0"),
                timestamp=event.timestamp or captured_at,
                dimensions=event.dimensions or {},
                raw={
                    "request_id": event.request_id,
                    "model_name": event.model_name,
                },
            )
            requests.append(request)

        metric_repo.create_inference_requests(db, requests)
        return len(requests)


ingest_service = IngestService()
