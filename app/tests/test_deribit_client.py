import pytest

from app.services.deribit_client import DeribitClient


@pytest.mark.asyncio
async def test_fetch_all_prices():
    """Проверяет, что метод fetch_all_prices возвращает словарь тикеров и цен (float)"""
    client = DeribitClient()
    prices = await client.fetch_all_prices()

    assert isinstance(prices, dict)
    for ticker, price in prices.items():
        assert isinstance(price, float)


@pytest.mark.asyncio
async def test_fetch_all_prices_mocked_fetch_price(monkeypatch):
    """Проверяет корректную работу fetch_all_prices при замоканном fetch_price"""

    async def mock_fetch_price(self, session, ticker):
        return 50000.0

    monkeypatch.setattr(DeribitClient, "fetch_price", mock_fetch_price)
    client = DeribitClient()
    prices = await client.fetch_all_prices()

    assert prices["btc_usd"] == 50000.0
