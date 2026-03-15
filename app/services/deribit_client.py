import aiohttp
import asyncio


DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_index_price"


class DeribitClient:
    """Получает цены с Deribit"""
    def __init__(self):
        self.tickers = ["btc_usd", "eth_usd"]

    async def fetch_price(self, session: aiohttp.ClientSession, ticker: str) -> float:
        params = {"index_name": ticker}

        async with session.get(DERIBIT_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            return data["result"]["index_price"]

    async def fetch_all_prices(self) -> dict[str, float]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, ticker) for ticker in self.tickers]
            results = await asyncio.gather(*tasks)
        return dict(zip(self.tickers, results))
