from sqlalchemy import BigInteger, Index
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.testing.schema import mapped_column

Base = declarative_base()


class Price(Base):
    """SQLAlchemy модель для хранения данных: id, тикер валюты, текущая цена, время (UNIX timestamp)"""

    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)
    __table_args__ = (Index("idx_ticker_timestamp", "ticker", "timestamp"),)
