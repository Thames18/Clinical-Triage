from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.workers.task import generate_triage_report
from celery.result import AsyncResult
from app.core.celeryapp import celery_app

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/generate")
def request_report(triage_result: dict, patient_id: str):
    task = generate_triage_report.delay(triage_result, patient_id)
    return {"task_id": task.id, "status": "queued"}

@router.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status, "result": result.result}

@router.get("/download/{task_id}")
def download_report(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.status != "SUCCESS":
        return {"error": "Report not ready", "status": result.status}
    return FileResponse(result.result["file_path"], media_type="application/pdf")