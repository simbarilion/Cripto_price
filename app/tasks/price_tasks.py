import asyncio

from app.core.logger import setup_logger
from app.services.price_fetcher import fetch_and_store_prices
from app.tasks.celery_app import celery

logger = setup_logger(__name__, log_to_console=True)


@celery.task
def fetch_and_save_prices():
    """Celery задача: запускает асинхронное получение цен"""
    logger.info("Celery task started")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(fetch_and_store_prices())
    finally:
        loop.close()
    logger.info("Celery task finished")
