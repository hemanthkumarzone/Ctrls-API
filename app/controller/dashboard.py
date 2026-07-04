"""Dashboard controller."""

from typing import Any

from fastapi import APIRouter

dashboard_controller = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_client_demo_dashboard() -> dict[str, Any]:
    """Return a polished hard-coded payload for client demos."""
    return {
        "summary": {
            "requests": 15821,
            "tokens": 12849321,
            "cost": 324.62,
            "successRate": 99.2,
            "avgLatency": 934,
        },
        "kpis": [
            {"label": "Total Requests", "value": "15.8K", "delta": "+12.4%", "trend": "up"},
            {"label": "Active Agents", "value": "24", "delta": "+3", "trend": "up"},
            {"label": "Total Cost", "value": "$324.62", "delta": "+8.1%", "trend": "up"},
            {"label": "Avg Latency", "value": "934ms", "delta": "-6.2%", "trend": "down"},
            {"label": "Success Rate", "value": "99.2%", "delta": "+0.4%", "trend": "up"},
            {"label": "Token Usage", "value": "12.8M", "delta": "+18.7%", "trend": "up"},
        ],
        "costTrend": [
            {"month": "Jan", "cost": 220000},
            {"month": "Feb", "cost": 240000},
            {"month": "Mar", "cost": 260000},
            {"month": "Apr", "cost": 285000},
            {"month": "May", "cost": 305000},
            {"month": "Jun", "cost": 324620},
        ],
        "providerUsage": [
            {"name": "OpenAI", "requests": 8421, "cost": 182.4, "latency": 840, "share": 52},
            {"name": "Anthropic", "requests": 3211, "cost": 64.2, "latency": 910, "share": 20},
            {"name": "Gemini", "requests": 4189, "cost": 78.0, "latency": 720, "share": 28},
        ],
        "recentExecutions": [
            {"id": "exec-1042", "name": "Customer Support Agent", "status": "Completed", "duration": "1.2s", "cost": "$12.40"},
            {"id": "exec-1041", "name": "Forecasting Copilot", "status": "Running", "duration": "0.8s", "cost": "$8.10"},
            {"id": "exec-1040", "name": "Invoice Analyzer", "status": "Failed", "duration": "2.4s", "cost": "$3.20"},
        ],
        "toolRegistry": [
            {"name": "RAG Retriever", "status": "Healthy", "latency": "42ms"},
            {"name": "Policy Guardrails", "status": "Healthy", "latency": "18ms"},
            {"name": "Cost Optimizer", "status": "Warning", "latency": "77ms"},
        ],
        "guardrails": [
            {"name": "Blocked Prompts", "value": 82, "tone": "warning"},
            {"name": "Moderated Content", "value": 71, "tone": "info"},
            {"name": "Policy Violations", "value": 11, "tone": "critical"},
        ],
        "ragStats": [
            {"name": "Knowledge Base Hits", "value": "94%"},
            {"name": "Chunk Retrieval", "value": "1.4M"},
            {"name": "Answer Quality", "value": "4.8/5"},
        ],
        "quickActions": [
            {"title": "Run cost scan", "description": "Inspect latest spend anomalies", "action": "scan"},
            {"title": "Open playbook", "description": "Review escalation workflow", "action": "playbook"},
            {"title": "Export report", "description": "Download the weekly AI ops summary", "action": "export"},
        ],
    }


def get_llm_ops_dashboard() -> dict[str, Any]:
    """Return a separate hard-coded payload for LLM operations demo tabs."""
    return {
        "summary": {
            "requests": 12480,
            "tokens": 9875421,
            "cost": 218.9,
            "successRate": 98.7,
            "avgLatency": 812,
        },
        "kpis": [
            {"label": "Prompt Volume", "value": "12.5K", "delta": "+9.3%", "trend": "up"},
            {"label": "Active Models", "value": "6", "delta": "+1", "trend": "up"},
            {"label": "LLM Cost", "value": "$218.90", "delta": "+5.6%", "trend": "up"},
            {"label": "Avg Response", "value": "812ms", "delta": "-4.1%", "trend": "down"},
            {"label": "Quality Score", "value": "98.7%", "delta": "+0.8%", "trend": "up"},
            {"label": "Context Tokens", "value": "9.9M", "delta": "+11.2%", "trend": "up"},
        ],
        "costTrend": [
            {"month": "Jan", "cost": 175000},
            {"month": "Feb", "cost": 185000},
            {"month": "Mar", "cost": 196000},
            {"month": "Apr", "cost": 205000},
            {"month": "May", "cost": 214000},
            {"month": "Jun", "cost": 218900},
        ],
        "providerUsage": [
            {"name": "Azure OpenAI", "requests": 6120, "cost": 112.4, "latency": 760, "share": 49},
            {"name": "Anthropic", "requests": 3010, "cost": 63.2, "latency": 840, "share": 24},
            {"name": "OpenAI", "requests": 3350, "cost": 43.3, "latency": 810, "share": 27},
        ],
        "recentExecutions": [
            {"id": "llm-2001", "name": "Policy Summarizer", "status": "Completed", "duration": "0.9s", "cost": "$9.40"},
            {"id": "llm-2000", "name": "Support Reply Draft", "status": "Running", "duration": "1.1s", "cost": "$6.20"},
            {"id": "llm-1999", "name": "Invoice Extraction", "status": "Failed", "duration": "2.1s", "cost": "$2.80"},
        ],
        "toolRegistry": [
            {"name": "Prompt Cache", "status": "Healthy", "latency": "24ms"},
            {"name": "Embedding Service", "status": "Healthy", "latency": "31ms"},
            {"name": "Guardrail Filter", "status": "Warning", "latency": "68ms"},
        ],
        "guardrails": [
            {"name": "Prompt Blocks", "value": 41, "tone": "warning"},
            {"name": "Unsafe Outputs", "value": 16, "tone": "info"},
            {"name": "Policy Escalations", "value": 7, "tone": "critical"},
        ],
        "ragStats": [
            {"name": "Context Retrieval", "value": "91%"},
            {"name": "Vector Hits", "value": "3.2M"},
            {"name": "Answer Faithfulness", "value": "4.6/5"},
        ],
        "quickActions": [
            {"title": "Review prompt pack", "description": "Inspect the latest prompt bundle", "action": "review"},
            {"title": "Tune model routing", "description": "Balance cost vs quality", "action": "route"},
            {"title": "Export evaluation", "description": "Download validation summaries", "action": "export"},
        ],
    }


@dashboard_controller.get("/summary")
def get_dashboard_summary() -> dict[str, Any]:
    return {
        "totalSpend": 284750.00,
        "monthOverMonthChange": 12.4,
        "forecastedSpend": 310000.00,
        "budgetLimit": 300000.00,
        "savingsOpportunity": 47200.00,
        "anomaliesDetected": 3,
    }


@dashboard_controller.get("/spend-trend")
def get_spend_trend() -> list[dict[str, Any]]:
    return [
        {"month": "Apr 2025", "compute": 95000, "storage": 48000, "network": 30000, "kubernetes": 35000, "database": 22000},
        {"month": "Mar 2026", "compute": 120000, "storage": 54000, "network": 38000, "kubernetes": 47000, "database": 25750},
    ]


@dashboard_controller.get("/cost-by-category")
def get_cost_by_category() -> list[dict[str, Any]]:
    return [
        {"name": "Compute", "value": 120000, "change": 8.2},
        {"name": "Storage", "value": 54000, "change": -3.1},
    ]


@dashboard_controller.get("/top-services")
def get_top_services() -> list[dict[str, Any]]:
    return [
        {"name": "EC2 Instances", "provider": "AWS", "cost": 68500, "usage": "1,240 vCPU-hours", "trend": 12.3},
    ]


@dashboard_controller.get("/recommendations-widget")
def get_recommendations_widget() -> list[dict[str, Any]]:
    return [
        {"id": "rec-1", "title": "Right-size EC2 instances in us-east-1", "category": "Compute", "impact": "High", "effort": "Low", "savings": 18500, "status": "open"},
        {"id": "rec-2", "title": "Resize GKE nodes", "category": "Kubernetes", "impact": "Medium", "effort": "Medium", "savings": 9200, "status": "open"},
        {"id": "rec-3", "title": "Archive unused snapshots", "category": "Storage", "impact": "Low", "effort": "Low", "savings": 4700, "status": "open"},
    ]


@dashboard_controller.get("/anomalies-widget")
def get_anomalies_widget() -> list[dict[str, Any]]:
    return [
        {"id": "anom-1", "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": "Critical", "spike": 340},
        {"id": "anom-2", "service": "S3 Storage", "detectedAt": "2026-03-18T10:10:00Z", "severity": "High", "spike": 120},
        {"id": "anom-3", "service": "RDS Instances", "detectedAt": "2026-03-20T09:22:00Z", "severity": "Medium", "spike": 65},
    ]


@dashboard_controller.get("/reports-widget")
def get_reports_widget() -> list[dict[str, Any]]:
    return [
        {"name": "Weekly Cost Summary", "frequency": "Weekly", "recipients": ["cfo@company.com"], "lastRun": "2026-03-10T08:00:00Z", "format": "PDF"},
    ]


@dashboard_controller.post("/refresh")
def refresh_dashboard() -> dict[str, Any]:
    return {"message": "Dashboard data refreshed.", "timestamp": "2026-03-25T13:00:00.000Z"}


@dashboard_controller.get("/sample")
def sample_dashboard():
    return {
        'data': [],
        'msg': "Dashboard data fetched successfully"
    }


@dashboard_controller.get("/agent-ops")
def agent_ops_dashboard() -> dict[str, Any]:
    """Return the agent operations demo payload."""
    return get_client_demo_dashboard()


@dashboard_controller.get("/llm-ops")
def llm_ops_dashboard() -> dict[str, Any]:
    """Return the LLM operations demo payload."""
    return get_llm_ops_dashboard()

