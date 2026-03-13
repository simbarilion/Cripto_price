from typing import List

from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Price
from app.schemas.price import PriceResponse

app = FastAPI(title="Crypto Prices API")

@app.get("/prices", response_model=List[PriceResponse])
def get_prices(ticker: str = Query(...)):
    """Получение всех данных по валюте"""
    db: Session = SessionLocal()
    prices = db.query(Price).filter(Price.ticker == ticker).all()
    db.close()
    return prices  # FastAPI сам конвертирует в PriceResponse через Pydantic модель


@app.get("/price/latest", response_model=PriceResponse)
def get_latest_price(ticker: str = Query(...)):
    """Получение последней цены"""
    db: Session = SessionLocal()
    price = db.query(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).first()
    db.close()
    if not price:
        raise HTTPException(status_code=404, detail="No data")
    return price


@app.get("/price/by-date", response_model=List[PriceResponse])
def get_price_by_date(
        ticker: str = Query(...),
        from_ts: int = Query(..., description="UNIX timestamp от"),
        to_ts: int = Query(..., description="UNIX timestamp до")):
    """Получение данных по дате"""
    db: Session = SessionLocal()
    prices = db.query(Price).filter(
        Price.ticker == ticker,
        Price.timestamp >= from_ts,
        Price.timestamp <= to_ts
    ).all()
    db.close()
    return prices
