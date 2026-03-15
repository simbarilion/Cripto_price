import aiohttp
import asyncio


DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_index_price"


class DeribitClient:
    """Получает цены с Deribit"""
    def __init__(self):
        self.tickers = ["btc_usd", "eth_usd"]

    async def fetch_price(self, session: aiohttp.ClientSession, ticker: str) -> float | None:
        params = {"index_name": ticker}

        try:
            async with session.get(DERIBIT_URL, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                return data["result"]["index_price"]

        except aiohttp.ClientError as e:
            logger.error(f"HTTP error for {ticker}: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout for {ticker}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error {ticker}: {e}")
            return None

    async def fetch_all_prices(self) -> dict[str, float]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, ticker) for ticker in self.tickers]
            results = await asyncio.gather(*tasks)
        return {
            ticker: price
            for ticker, price in zip(self.tickers, results)
            if price is not None
        }
