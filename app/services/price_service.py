import time

from app.db.database import SessionLocal
from app.db.models import Price


def save_price(ticker: str, price: float):
    db = SessionLocal()
    db_price = Price(
        ticker=ticker,
        price=price,
        timestamp=int(time.time())
    )
    db.add(db_price)
    db.commit()
    db.close()
