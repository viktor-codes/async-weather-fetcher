from celery import Celery
from app.core.config import settings

celery = Celery(
    "weather_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery.conf.update(task_track_started=True)
