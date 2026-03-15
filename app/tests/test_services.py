from app.db.database import SessionLocal
from app.db.models import Price
from app.services.price_service import save_price


def test_save_price():
    ticker = "btc_usd"
    price = 50000

    save_price(ticker, price)

    db = SessionLocal()

    result = db.query(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).first()

    db.close()

    assert result is not None
    assert result.price == price
