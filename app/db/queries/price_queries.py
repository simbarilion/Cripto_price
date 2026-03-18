import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.db.models import Price

logger = setup_logger(__name__, log_to_console=True)


class PriceRepository:

    def get_prices(self, db: Session, ticker: str, limit: int, offset: int):
        """
        SQL-запрос: выбирает цены для тикера
        Args:
            db: SQLAlchemy Session
            ticker: тикер валюты
            limit: количество записей
            offset: смещение
        Returns:
            Список Price ORM объектов
        """
        query = (
            select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc()).limit(limit).offset(offset)
        )
        return db.scalars(query).all()

    def get_latest_price(self, db: Session, ticker: str):
        """
        SQL-запрос: выбирает последнюю цену для тикера
        Args:
            db: SQLAlchemy Session
            ticker: тикер валюты
        Returns:
            Price ORM объект
        """
        query = select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc())
        return db.scalars(query).first()

    def get_price_by_date(self, db: Session, ticker: str, from_ts: int, to_ts: int, limit: int, offset: int):
        """
        SQL-запрос: выбирает цены для тикера по дате
        Args:
            db: SQLAlchemy Session
            ticker: тикер валюты
            from_ts: начальная дата диапазона
            to_ts: конечная дата диапазона
            limit: количество записей
            offset: смещение
        Returns:
            Список Price ORM объектов
        """
        query = (
            select(Price)
            .where(Price.ticker == ticker, Price.timestamp.between(from_ts, to_ts))
            .order_by(Price.timestamp)
            .limit(limit)
            .offset(offset)
        )
        return db.scalars(query).all()

    def save_price(self, db: Session, ticker: str, price: float):
        """
        SQL-запрос: cохраняет цену тикера с текущей датой
        Args:
            db: SQLAlchemy Session
            ticker: тикер валюты
            price: цена тикера
            Returns:
                None
        """
        db_price = Price(ticker=ticker, price=price, timestamp=int(time.time()))
        db.add(db_price)

    def save_prices_batch(self, db: Session, prices: dict[str, float]):
        """
        SQL-запрос: cохраняет цены тикеров с текущей датой
        Args:
            db: SQLAlchemy Session
            prices: тикер: цена тикера
            Returns:
                None
        """
        db.add_all([Price(ticker=t, price=p, timestamp=int(time.time())) for t, p in prices.items()])
