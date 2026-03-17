from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.db.queries.price_queries import PriceRepository

logger = setup_logger(__name__, log_to_console=True)


class PriceService:

    def __init__(self):
        self.repo = PriceRepository()

    def get_prices(self, db: Session, ticker: str, limit: int, offset: int):
        return self.repo.get_prices(db, ticker, limit, offset)

    def get_latest_price(self, db: Session, ticker: str):
        price = self.repo.get_latest_price(db, ticker)
        if not price:
            logger.error("No price data found for %s", ticker)
            raise HTTPException(status_code=404, detail="No data")
        return price

    def get_price_by_date(self, db: Session, ticker: str, limit: int, from_ts: int, to_ts: int):
        if from_ts > to_ts:
            raise ValueError("from_ts must be less than to_ts")
        return self.repo.get_price_by_date(db, ticker, limit, from_ts, to_ts)

    def save_price(self, db: Session, ticker: str, price: float):
        self.repo.save_price(db, ticker, price)

    # def save_prices_batch(self, db: Session, prices: dict[str, float]):
    #     self.repo.save_prices_batch(db, prices)
