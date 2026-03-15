from unittest.mock import patch

import pytest

from app.services.price_fetcher import fetch_and_store_prices


@pytest.mark.asyncio
async def test_fetch_and_store():
    """Проверяет, что fetch_and_store_prices вызывает save_price 2 раза"""
    with patch("app.services.price_fetcher.DeribitClient.fetch_all_prices") as mock_fetch:
        mock_fetch.return_value = {"btc_usd": 65000, "eth_usd": 3000}

        with patch("app.services.price_fetcher.save_price") as mock_save:
            await fetch_and_store_prices()
            assert mock_fetch.called
            assert mock_save.call_count == 2
            mock_save.assert_any_call("btc_usd", 65000)
            mock_save.assert_any_call("eth_usd", 3000)
