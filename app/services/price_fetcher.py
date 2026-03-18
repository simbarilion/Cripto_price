from app.core.logger import setup_logger
from app.db.database import SessionLocal
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService

logger = setup_logger(__name__, log_to_console=True)

service = PriceService()


async def fetch_and_store_prices():
    """Асинхронный сервисный слой: получает актуальные цены из Deribit и сохраняет в базе данных"""
    client = DeribitClient()
    prices = await client.fetch_all_prices()
    if not prices:
        logger.warning("No prices received from Deribit")
        return
    logger.info("Fetched %d from Deribit", len(prices))

    db = SessionLocal()
    try:
        service.save_prices_batch(db, prices)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error("Failed to save prices: %s", e)
    finally:
        db.close()
