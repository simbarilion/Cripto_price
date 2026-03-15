import asyncio
from app.services.price_fetcher import fetch_and_store_prices
from app.tasks.celery_app import celery


@celery.task
def fetch_and_save_prices():
    """Вызывает сервисный слой"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(fetch_and_store_prices())
    finally:
        loop.close()
