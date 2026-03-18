from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.db.queries.price_queries import PriceRepository

logger = setup_logger(__name__, log_to_console=True)


class PriceService:

    def __init__(self):
        self.repo = PriceRepository()

    def get_prices(self, db: Session, ticker: str, limit: int, offset: int):
        """Получает цены для тикера с пагинацией"""
        logger.info("Request data for %s", ticker)
        return self.repo.get_prices(db, ticker, limit, offset)

    def get_latest_price(self, db: Session, ticker: str):
        """Получает последнюю цену тикера"""
        logger.info("Request latest price for %s", ticker)
        price = self.repo.get_latest_price(db, ticker)
        if not price:
            logger.error("No price data found for %s", ticker)
            raise HTTPException(status_code=404, detail="No data")
        return price

    def get_price_by_date(self, db: Session, ticker: str, from_ts: int, to_ts: int, limit: int, offset: int):
        """Получает цены для тикера по дате с пагинацией"""
        logger.info("Request price for %s", ticker)
        if from_ts > to_ts:
            raise ValueError("from_ts must be less than to_ts")
        return self.repo.get_price_by_date(db, ticker, from_ts, to_ts, limit, offset)

    def save_price(self, db: Session, ticker: str, price: float):
        """Сохраняет цену тикера в базе данных"""
        self.repo.save_price(db, ticker, price)
        logger.info("Saved %s prices to DB", price)

    def save_prices_batch(self, db: Session, prices: dict[str, float]):
        """Сохраняет цены тикеров в базе данных"""
        try:
            self.repo.save_prices_batch(db, prices)
            logger.info("Saved %d prices to DB", len(prices))
        except Exception as e:
            logger.error("Failed to save prices: %s", e)
            raise
