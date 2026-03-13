from celery import Celery
from celery.schedules import crontab
import os

from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL")
)

celery.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.price_tasks.fetch_and_save_prices",
        "schedule": crontab(minute="*"),
    }
}

celery.conf.timezone = "UTC"
