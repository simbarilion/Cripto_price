import pytest

from app.services.deribit_client import DeribitClient


@pytest.mark.asyncio
async def test_fetch_all_prices():
    client = DeribitClient()

    prices = await client.fetch_all_prices()

    assert isinstance(prices, dict)

    for ticker, price in prices.items():
        assert isinstance(price, float)
