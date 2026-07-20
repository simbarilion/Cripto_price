import time

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import setup_logger
from app.db.models import Price

logger = setup_logger(__name__, log_to_console=True)


class PriceRepository:

    async def get_prices(self, db: AsyncSession, ticker: str, limit: int, offset: int):
        """
        SQL-запрос: выбирает цены для тикера
        Args:
            db: AsyncSession
            ticker: тикер валюты
            limit: количество записей
            offset: смещение
        Returns:
            Список Price ORM объектов
        """
        query = (
            select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc()).limit(limit).offset(offset)
        )
        result = await db.scalars(query)
        return result.all()

    async def get_latest_price(self, db: AsyncSession, ticker: str):
        """
        SQL-запрос: выбирает последнюю цену для тикера
        Args:
            db: AsyncSession
            ticker: тикер валюты
        Returns:
            Price ORM объект
        """
        query = select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc())
        result = await db.scalars(query)
        return result.first()

    async def get_price_by_date(
        self, db: AsyncSession, ticker: str, from_ts: int, to_ts: int, limit: int, offset: int
    ):
        """
        SQL-запрос: выбирает цены для тикера по дате
        Args:
            db: AsyncSession
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
        result = await db.scalars(query)
        return result.all()

    async def save_prices_batch(self, db: AsyncSession, prices: dict[str, float]):
        """
        SQL-запрос: cохраняет цены тикеров с текущей датой
        Args:
            db: AsyncSession
            prices: тикер: цена тикера
            Returns:
                None
        """
        timestamp = int(time.time())
        query = insert(Price).values([{"ticker": t, "price": p, "timestamp": timestamp} for t, p in prices.items()])
        await db.execute(query)
