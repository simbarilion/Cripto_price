from sqlalchemy import BigInteger, Column, Float, Index, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Price(Base):
    """SQLAlchemy модель для хранения данных: id, тикер валюты, текущая цена, время (UNIX timestamp)"""

    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(BigInteger, index=True)
    __table_args__ = (
        Index("idx_ticker_timestamp", "ticker", "timestamp"),
    )  # составной индекс ускорит выборку WHERE ticker=... AND timestamp BETWEEN
