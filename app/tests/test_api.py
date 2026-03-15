from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_prices_empty():
    response = client.get("/prices?ticker=btc_usd")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_latest_price_not_found():
    response = client.get("/price/latest?ticker=unknown")

    assert response.status_code == 404
