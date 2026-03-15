from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.db.database import get_db
from app.main import app

client = TestClient(app)


def override_get_db():
    mock_db = MagicMock()
    yield mock_db


app.dependency_overrides[get_db] = override_get_db


def test_get_prices_empty():
    response = client.get("/prices?ticker=btc_usd")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
