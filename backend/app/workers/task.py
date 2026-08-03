from app.core.celery_app import celery_app
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

REPORTS_DIR = "app/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

@celery_app.task(bind=True, name="generate_triage_report")
def generate_triage_report(self, triage_result: dict, patient_id: str):
    filename = f"{REPORTS_DIR}/triage_{patient_id}_{self.request.id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Clinical Triage Report")
    c.setFont("Helvetica", 11)

    y = 710
    for key, value in triage_result.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()
    return {"status": "complete", "file_path": filename}