import asyncio
from app.services.price_fetcher import run_async_fetch
from app.tasks.celery_app import celery


@celery.task
def fetch_and_save_prices():
    asyncio.run(run_async_fetch())
