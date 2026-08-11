from pathlib import Path
from fastapi import APIRouter
from app.core.metrics import metrics
from app.core.version import version_info

router = APIRouter(tags=["system"])

@router.get("/health/live")
def liveness():
    return {"status": "alive"}

@router.get("/health/ready")
def readiness():
    return {
        "status": "ready",
        "evidence_directory_exists": Path("data/evidence").exists(),
        "version": version_info(),
    }

@router.get("/metrics")
def prometheus_metrics():
    snapshot = metrics.snapshot()
    lines = [
        "# HELP clinical_triage_requests_total Total HTTP requests.",
        "# TYPE clinical_triage_requests_total counter",
        f"clinical_triage_requests_total {snapshot['requests_total']}",
        "# HELP clinical_triage_errors_total Total HTTP 5xx responses.",
        "# TYPE clinical_triage_errors_total counter",
        f"clinical_triage_errors_total {snapshot['errors_total']}",
        "# HELP clinical_triage_average_latency_ms Average recent request latency.",
        "# TYPE clinical_triage_average_latency_ms gauge",
        f"clinical_triage_average_latency_ms {snapshot['average_latency_ms']}",
    ]
    for level, count in snapshot["triage_levels"].items():
        lines.append(f'clinical_triage_results_total{{triage_level="{level}"}} {count}')
    return "\n".join(lines) + "\n"
