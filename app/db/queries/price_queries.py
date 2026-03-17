import time

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.db.models import Price

logger = setup_logger(__name__, log_to_console=True)


class PriceRepository:

    def get_prices(self, db: Session, ticker: str, limit: int, offset: int):
        """Возвращает все данные по валюте"""
        logger.info("Request data for %s", ticker)
        query = (
            select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc()).limit(limit).offset(offset)
        )
        return db.scalars(query).all()

    def get_latest_price(self, db: Session, ticker: str):
        """Возвращает последнюю цену валюты"""
        logger.info("Request latest price for %s", ticker)
        query = select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc())
        price = db.scalars(query).first()
        if not price:
            logger.error("No price data found for %s", ticker)
            raise HTTPException(status_code=404, detail="No data")
        return price

    def get_price_by_date(self, db: Session, ticker: str, limit: int, from_ts: int, to_ts: int):
        """Возвращает цену валюты с фильтром по дате"""
        logger.info("Request price for %s", ticker)
        if from_ts > to_ts:
            raise HTTPException(status_code=400, detail="from_ts must be less than to_ts")
        query = (
            select(Price)
            .where(Price.ticker == ticker, Price.timestamp.between(from_ts, to_ts))
            .order_by(Price.timestamp)
            .limit(limit)
        )
        return db.scalars(query).all()

    def save_price(self, db: Session, ticker: str, price: float):
        """Сохраняет данные о цене валюты с текущей датой в БД"""
        db_price = Price(ticker=ticker, price=price, timestamp=int(time.time()))
        db.add(db_price)

    # def save_prices_batch(self, db: Session, prices: dict[str, float]):
    #     """Сохраняет данные о ценах валют с текущей датой в БД"""
    #     timestamp = int(time.time())
    #
    #     objects = [Price(ticker=t, price=p, timestamp=timestamp) for t, p in prices.items()]
    #     db.add_all(objects)
