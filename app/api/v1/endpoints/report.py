"""
Report endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from datetime import datetime

router = APIRouter()


@router.get("/")
async def get_reports(db: Session = Depends(deps.get_db)):
    """Get all reports."""
    return [
        {
            "name": "Weekly Cost Summary",
            "frequency": "Weekly",
            "recipients": ["cfo@company.com"],
            "last_run": "2026-03-10T08:00:00Z",
            "format": "PDF",
        },
        {
            "name": "Monthly K8s Report",
            "frequency": "Monthly",
            "recipients": ["devops@company.com"],
            "last_run": "2026-03-01T08:00:00Z",
            "format": "CSV",
        },
    ]


@router.get("/{report_id}")
async def get_report(report_id: str, db: Session = Depends(deps.get_db)):
    """Get specific report."""
    return {
        "id": report_id,
        "name": "Weekly Cost Summary",
        "frequency": "Weekly",
        "recipients": ["cfo@company.com"],
        "last_run": "2026-03-10T08:00:00Z",
        "format": "PDF",
    }


@router.post("/create", response_model=dict)
async def create_report(
    report: schemas.ReportCreate, db: Session = Depends(deps.get_db)
):
    """Create new report."""
    return {
        "id": "rpt-1711361400000",
        "message": "Report created successfully.",
    }


@router.put("/{report_id}/update")
async def update_report(
    report_id: str,
    report_update: schemas.ReportUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update report."""
    return {
        "name": "Weekly Cost Summary",
        "updated": True,
        "recipients": report_update.recipients or ["cfo@company.com"],
    }


@router.delete("/{report_id}")
async def delete_report(report_id: str, db: Session = Depends(deps.get_db)):
    """Delete report."""
    return {"message": f"Report {report_id} deleted."}


@router.post("/{report_id}/generate")
async def generate_report(report_id: str, db: Session = Depends(deps.get_db)):
    """Generate report."""
    return {
        "message": "Report generation started.",
        "job_id": "job-1711361400000",
    }


@router.get("/{report_id}/download")
async def download_report(report_id: str, db: Session = Depends(deps.get_db)):
    """Download report."""
    return {"download_url": f"/exports/{report_id}_report.pdf"}


@router.get("/schedules")
async def get_report_schedules(db: Session = Depends(deps.get_db)):
    """Get report schedules."""
    return [
        {
            "name": "Weekly Cost Summary",
            "frequency": "Weekly",
            "last_run": "2026-03-10T08:00:00Z",
        },
        {
            "name": "Monthly K8s Report",
            "frequency": "Monthly",
            "last_run": "2026-03-01T08:00:00Z",
        },
    ]
