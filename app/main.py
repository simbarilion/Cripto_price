from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.db.database import get_db
from app.db.models import Price
from app.schemas.price import PriceResponse

logger = setup_logger(__name__, log_to_console=True)
app = FastAPI(title="Crypto Prices API")


@app.get("/prices", response_model=List[PriceResponse])
def get_prices(
    ticker: str = Query(...), limit: int = Query(100, le=1000), offset: int = Query(0), db: Session = Depends(get_db)
):
    """Возвращает все данные по валюте"""
    logger.info("Request data for %s", ticker)
    prices = (
        db.query(Price)
        .filter(Price.ticker == ticker)
        .order_by(Price.timestamp.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return prices


@app.get("/price/latest", response_model=PriceResponse)
def get_latest_price(ticker: str = Query(...), db: Session = Depends(get_db)):
    """Возвращает последнюю цену валюты"""
    logger.info("Request latest price for %s", ticker)
    price = db.query(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).first()
    if not price:
        logger.error("No price data found for %s", ticker)
        raise HTTPException(status_code=404, detail="No data")
    return price


@app.get("/price/by-date", response_model=List[PriceResponse])
def get_price_by_date(
    ticker: str = Query(...), from_ts: int = Query(...), to_ts: int = Query(...), db: Session = Depends(get_db)
):
    """Возвращает цену валюты с фильтром по дате"""
    logger.info("Request price for %s", ticker)
    if from_ts > to_ts:
        raise HTTPException(status_code=400, detail="from_ts must be less than to_ts")
    prices = (
        db.query(Price)
        .filter(Price.ticker == ticker, Price.timestamp >= from_ts, Price.timestamp <= to_ts)
        .order_by(Price.timestamp)
        .all()
    )
    return prices
