"""Anomalies controller."""

from typing import Any

from fastapi import APIRouter, Body

anomalies_controller = APIRouter(prefix="/anomalies", tags=["Anomalies"])


@anomalies_controller.get("")
def get_anomalies() -> list[dict[str, Any]]:
    return [
        {"id": "anom-1", "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": "Critical", "spike": 340, "description": "Sudden 340% spike in Lambda invocations.", "data": [10, 12, 11, 13, 12, 45, 48]},
    ]


@anomalies_controller.get("/{anomaly_id}")
def get_anomaly(anomaly_id: str) -> dict[str, Any]:
    return {"id": anomaly_id, "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": "Critical", "spike": 340, "description": "Sudden 340% spike in Lambda invocations.", "data": [10, 12, 11, 13, 12, 45, 48]}


@anomalies_controller.get("/filter")
def filter_anomalies(severity: str | None = None) -> list[dict[str, Any]]:
    return [{"id": "anom-1", "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": severity or "Critical", "spike": 340}]


@anomalies_controller.get("/severity")
def get_anomalies_severity() -> list[dict[str, Any]]:
    return [{"severity": "Critical", "count": 1}, {"severity": "High", "count": 2}, {"severity": "Medium", "count": 2}]


@anomalies_controller.put("/{anomaly_id}/acknowledge")
def acknowledge_anomaly(anomaly_id: str) -> dict[str, Any]:
    return {"id": anomaly_id, "status": "acknowledged"}


@anomalies_controller.put("/{anomaly_id}/resolve")
def resolve_anomaly(anomaly_id: str) -> dict[str, Any]:
    return {"id": anomaly_id, "status": "resolved"}


@anomalies_controller.get("/{anomaly_id}/investigate")
def investigate_anomaly(anomaly_id: str) -> dict[str, Any]:
    return {"id": anomaly_id, "investigation": {"steps": ["Review CloudWatch logs", "Check billing dashboard", "Notify team lead"]}}


@anomalies_controller.get("/timeline")
def get_anomalies_timeline() -> list[dict[str, Any]]:
    return [{"id": "anom-1", "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": "Critical", "spike": 340}]


@anomalies_controller.get("/statistics")
def get_anomalies_statistics() -> dict[str, Any]:
    return {"total": 5, "avgSpike": 150, "bySeverity": {"Critical": 1, "High": 2, "Medium": 2}}


@anomalies_controller.get("/alerts-summary")
def get_alerts_summary() -> dict[str, Any]:
    return {"active": 5, "acknowledged": 0, "resolved": 0}


@anomalies_controller.get("/sample")
def sample_anomalies():
    return {
        'data': [],
        'msg': "Anomalies fetched successfully"
    }

