from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "clinical_triage",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    task_track_started=True,
    task_send_sent_event=True,
)