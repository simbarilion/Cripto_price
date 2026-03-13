from app.services.deribit_client import DeribitClient
from app.services.price_service import save_price


async def fetch_and_store_prices():
    """Async сервисный слой: соединяет DeribitClient + PriceService"""
    client = DeribitClient()
    prices = await client.fetch_all_prices()
    for ticker, price in prices.items():
        save_price(ticker, price)
