import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# Celery конфигурация
celery = Celery("worker", broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

celery.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.price_tasks.fetch_and_save_prices",
        "schedule": crontab(minute="*"),
    }
}

celery.conf.timezone = "UTC"
