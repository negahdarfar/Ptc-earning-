import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    with TestClient(app) as test_client:
        yield test_client


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_private_reads_reject_missing_token(client):
    for path in ("/summary", "/opportunities", "/revenue"):
        assert client.get(path).status_code == 401


def test_private_reads_reject_wrong_token(client):
    response = client.get("/summary", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 401


def test_correct_bearer_token_can_read_private_data(client):
    response = client.get("/summary", headers={"Authorization": "Bearer test-secret-token"})
    assert response.status_code == 200


def test_write_requires_bearer_token(client):
    payload = {
        "name": "Example Platform",
        "category": "affiliate",
        "platform_url": "https://example.com",
    }
    assert client.post("/opportunities", json=payload).status_code == 401
    response = client.post(
        "/opportunities",
        json=payload,
        headers={"Authorization": "Bearer test-secret-token"},
    )
    assert response.status_code == 201


def test_missing_server_token_fails_closed(client, monkeypatch):
    monkeypatch.delenv("EARNORBIT_API_TOKEN")
    response = client.get("/summary")
    assert response.status_code == 503
