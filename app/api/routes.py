from typing import List

from fastapi import APIRouter

from app.api.dependencies import DBSession, From_ts, Limit, Offset, Ticker, To_ts
from app.core.logger import setup_logger
from app.schemas.price import PriceResponse
from app.services.price_service import PriceService

router = APIRouter(prefix="/prices", tags=["Получение цен криптовалют с биржи Deribit"])

logger = setup_logger(__name__, log_to_console=True)

service = PriceService()


@router.get("/", response_model=List[PriceResponse], summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_prices(db: DBSession, ticker: Ticker, limit: Limit, offset: Offset):
    """Возвращает все данные по валюте"""
    logger.info("Request data for %s", ticker)
    return service.get_prices(db, ticker, limit, offset)


@router.get("/latest", response_model=PriceResponse, summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_latest_price(db: DBSession, ticker: Ticker):
    """Возвращает последнюю цену валюты"""
    logger.info("Request latest price for %s", ticker)
    return service.get_latest_price(db, ticker)


@router.get("/by-date", response_model=List[PriceResponse], summary="Поддерживаемые тикеры: btc_usd, eth_usd")
def get_price_by_date(db: DBSession, ticker: Ticker, limit: Limit, from_ts: From_ts, to_ts: To_ts):
    """Возвращает цену валюты с фильтром по дате"""
    logger.info("Request price for %s", ticker)
    return service.get_price_by_date(db, ticker, limit, from_ts, to_ts)
