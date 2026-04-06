import asyncio

import aiohttp

from app.core.config import DERIBIT_URL, TICKERS
from app.core.logger import setup_logger

logger = setup_logger(__name__, log_to_console=True)


class DeribitClient:
    """Асинхронный клиент для получения цен криптовалютных индексов с Deribit"""

    def __init__(self):
        self.tickers = TICKERS
        self.semaphore = asyncio.Semaphore(50)  # ограничивает максимум 50 задач одновременно

    async def fetch_price(self, session: aiohttp.ClientSession, ticker: str) -> float | None:
        """Получает цену для одного тикера через Deribit API"""
        async with self.semaphore:
            params = {"index_name": ticker}

            try:
                async with session.get(DERIBIT_URL, params=params, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    price = data["result"]["index_price"]
                    logger.info("Received price for %s: %s", ticker, price)
                    return price

            except aiohttp.ClientError as e:
                logger.error("HTTP error for %s: %s", ticker, e)
                return None
            except asyncio.TimeoutError:
                logger.error("Timeout for %s", ticker)
                return None
            except Exception as e:
                logger.error("Unexpected error for %s: %s", ticker, e)
                return None

    async def fetch_all_prices(self) -> dict[str, float]:
        """Получает цены для всех указанных тикеров валют"""
        connector = aiohttp.TCPConnector(
            limit=50,  # общее количество одновременных соединений
            limit_per_host=50,  # количество одновременных соединений к одному ресурсу
        )
        timeout = aiohttp.ClientTimeout(total=10)  # глобальный таймаут для сессии (подключение и ответ)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [self.fetch_price(session, ticker) for ticker in self.tickers]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        return {ticker: price for ticker, price in zip(self.tickers, results) if price is not None}
