import asyncio
from app.services.price_fetcher import fetch_and_store_prices
from app.tasks.celery_app import celery


@celery.task
def fetch_and_save_prices():
    """Вызывает сервисный слой"""
    asyncio.run(fetch_and_store_prices())
