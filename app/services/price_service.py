import time

from app.core.logger import setup_logger
from app.db.database import SessionLocal
from app.db.models import Price


logger = setup_logger(__name__, log_to_console=True)

def save_price(ticker: str, price: float):
    """Сохраняет данные о ценах валют с текущей датой в БД"""
    db = SessionLocal()
    try:
        db_price = Price(
            ticker=ticker,
            price=price,
            timestamp=int(time.time())
        )
        db.add(db_price)
        db.commit()
        logger.info("Saved price for %s: %s", ticker, price)
    except Exception as e:
        logger.error("Failed to save price for %s: %s", ticker, e)
    finally:
        db.close()
