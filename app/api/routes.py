from typing import List

from fastapi import APIRouter

from app.api.dependencies import DBSession, From_ts, Limit, Offset, Ticker, To_ts
from app.schemas.price import PriceResponse
from app.services.price_service import PriceService

router = APIRouter(prefix="/prices", tags=["Получение цен криптовалют с биржи Deribit"])

service = PriceService()


@router.get("/", response_model=List[PriceResponse], summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_prices(db: DBSession, ticker: Ticker, limit: Limit = 100, offset: Offset = 0):
    """Возвращает список цен для указанного тикера"""
    return service.get_prices(db, ticker, limit, offset)


@router.get("/latest", response_model=PriceResponse, summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_latest_price(db: DBSession, ticker: Ticker):
    """Возвращает последнюю цену указанного тикера"""
    return service.get_latest_price(db, ticker)


@router.get("/by-date", response_model=List[PriceResponse], summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_price_by_date(
    db: DBSession, ticker: Ticker, from_ts: From_ts, to_ts: To_ts, limit: Limit = 100, offset: Offset = 0
):
    """Возвращает список цен для указанного тикера с фильтром по дате"""
    return service.get_price_by_date(db, ticker, from_ts, to_ts, limit, offset)
