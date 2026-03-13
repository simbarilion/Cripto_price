from app.services.deribit_client import DeribitClient
from app.services.price_service import save_price


async def run_async_fetch():

    client = DeribitClient()

    prices = await client.fetch_all_prices()

    for ticker, price in prices.items():
        save_price(ticker, price)
