import time

import aiohttp
import asyncio

from app.db.database import SessionLocal
from app.db.models import Price

DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_index_price"


class DeribitClient:
    def __init__(self):
        self.tickers = ["btc_usd", "eth_usd"]

    async def fetch_price(self, ticker: str) -> float:
        async with aiohttp.ClientSession() as session:
            params = {"index_name": ticker}
            async with session.get(DERIBIT_URL, params=params) as response:
                data = await response.json()
                return data["result"]["index_price"]

    async def fetch_all_prices(self) -> dict:
        tasks = [self.fetch_price(ticker) for ticker in self.tickers]
        results = await asyncio.gather(*tasks)
        return dict(zip(self.tickers, results))


def save_price(ticker: str, price: float):
    db = SessionLocal()
    db_price = Price(
        ticker=ticker,
        price=price,
        timestamp=int(time.time())
    )
    db.add(db_price)
    db.commit()
    db.close()


if __name__ == "__main__":
    client = DeribitClient()
    prices = asyncio.run(client.fetch_all_prices())
    for ticker, price in prices.items():
        save_price(ticker, price)
    print(prices)
