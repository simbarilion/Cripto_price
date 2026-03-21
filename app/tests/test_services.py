from unittest.mock import patch

import pytest

from app.services.price_fetcher import fetch_and_store_prices


@pytest.mark.asyncio
async def test_fetch_and_store():
    """Проверяет, что fetch_and_store_prices вызывает save_prices_batch 1 раз с правильными данными"""
    with patch("app.services.price_fetcher.DeribitClient.fetch_all_prices") as mock_fetch:
        mock_fetch.return_value = {"btc_usd": 65000, "eth_usd": 3000}

        with patch("app.services.price_fetcher.service.save_prices_batch") as mock_save:
            await fetch_and_store_prices()
            mock_save.assert_called_once()
            args, kwargs = mock_save.call_args
            db_arg, prices_arg = args
            assert prices_arg == {"btc_usd": 65000, "eth_usd": 3000}
