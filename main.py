from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Price


app = FastAPI(title="Crypto Prices API")

# Получение всех данных по валюте
@app.get("/prices")
def get_prices(ticker: str = Query(...)):
    db: Session = SessionLocal()
    prices = db.query(Price).filter(Price.ticker == ticker).all()
    db.close()
    return [{"price": p.price, "timestamp": p.timestamp} for p in prices]

# Получение последней цены
@app.get("/price/latest")
def get_latest_price(ticker: str = Query(...)):
    db: Session = SessionLocal()
    price = db.query(Price).filter(Price.ticker == ticker).order_by(Price.timestamp.desc()).first()
    db.close()
    if not price:
        raise HTTPException(status_code=404, detail="No data")
    return {"price": price.price, "timestamp": price.timestamp}

# Получение по дате
@app.get("/price/by-date")
def get_price_by_date(ticker: str = Query(...), from_ts: int = Query(...), to_ts: int = Query(...)):
    db: Session = SessionLocal()
    prices = db.query(Price).filter(
        Price.ticker == ticker,
        Price.timestamp >= from_ts,
        Price.timestamp <= to_ts
    ).all()
    db.close()
    return [{"price": p.price, "timestamp": p.timestamp} for p in prices]

# async def main():
#     """FastAPI сервер"""
#     client = DeribitClient()
#     prices = await client.fetch_all_prices()
#     print(prices)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())


# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# def root():
#     return {"message": "Crypto API running"}