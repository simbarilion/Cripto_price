from typing import List

from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Price
from app.schemas.price import PriceResponse

app = FastAPI(title="Crypto Prices API")

@app.get("/prices", response_model=List[PriceResponse])
def get_prices(
        ticker: str = Query(...),
        db: Session = Depends(get_db)
):
    """Получение всех данных по валюте"""
    prices = db.query(Price).filter(Price.ticker == ticker).all()
    return prices  # FastAPI сам конвертирует в PriceResponse через Pydantic модель


@app.get("/price/latest", response_model=PriceResponse)
def get_latest_price(
        ticker: str = Query(...),
        db: Session = Depends(get_db)
):
    """Получение последней цены"""
    price = db.query(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).first()
    if not price:
        raise HTTPException(status_code=404, detail="No data")
    return price


@app.get("/price/by-date", response_model=List[PriceResponse])
def get_price_by_date(
        ticker: str = Query(...),
        from_ts: int = Query(..., description="UNIX timestamp от"),
        to_ts: int = Query(..., description="UNIX timestamp до"),
        db: Session = Depends(get_db)
):
    """Получение данных по дате"""
    prices = db.query(Price).filter(
        Price.ticker == ticker,
        Price.timestamp >= from_ts,
        Price.timestamp <= to_ts
    ).all()
    return prices
