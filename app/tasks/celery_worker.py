from celery import Celery
from dotenv import load_dotenv


celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)
