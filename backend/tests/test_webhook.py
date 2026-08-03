import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app
from app.config import settings


@pytest.fixture
def client():
    with patch("main.telegram_app.initialize", new_callable=AsyncMock), \
         patch("main.telegram_app.start", new_callable=AsyncMock), \
         patch("main.telegram_app.stop", new_callable=AsyncMock), \
         patch("main.telegram_app.shutdown", new_callable=AsyncMock), \
         patch.object(settings, "USE_WEBHOOK", False):
        with TestClient(app) as c:
            yield c


def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "relu-backend"}


def test_webhook_unauthorized_token(client):
    with patch.object(settings, "WEBHOOK_SECRET_TOKEN", "super-secret"):
        response = client.post("/webhook", headers={"X-Telegram-Bot-Api-Secret-Token": "wrong-secret"})
        assert response.status_code == 403


def test_webhook_successful_process(client):
    sample_update = {
        "update_id": 10001,
        "message": {
            "message_id": 1,
            "date": 1441645532,
            "chat": {"id": 1111, "type": "private"},
            "text": "Hola bot"
        }
    }
    with patch("main.telegram_app.process_update", new_callable=AsyncMock) as mock_process:
        response = client.post("/webhook", json=sample_update)
        assert response.status_code == 200
        assert mock_process.called
