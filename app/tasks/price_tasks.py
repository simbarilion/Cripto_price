import asyncio

from app.core.logger import setup_logger
from app.services.price_fetcher import fetch_and_store_prices
from app.tasks.celery_app import celery_app

logger = setup_logger(__name__, log_to_console=True)


@celery_app.task
def fetch_and_save_prices():
    """Celery задача: запускает асинхронное получение цен"""
    logger.info("Celery task started")
    try:
        asyncio.run(fetch_and_store_prices())
    except Exception:
        logger.exception("Celery task failed")
    logger.info("Celery task finished")
