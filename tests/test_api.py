import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.database import get_session
from app.main import app


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def auth():
    return {"Authorization": "Bearer test-secret-token"}


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_private_reads_reject_missing_token(client):
    for path in ("/summary", "/opportunities", "/revenue", "/opportunities/recommended"):
        assert client.get(path).status_code == 401


def test_private_reads_reject_wrong_token(client):
    assert client.get("/summary", headers={"Authorization": "Bearer wrong"}).status_code == 401


def test_correct_bearer_token_can_read_private_data(client):
    assert client.get("/summary", headers=auth()).status_code == 200


def test_write_requires_bearer_token(client):
    payload = {"name": "Example Platform", "category": "affiliate", "platform_url": "https://example.com"}
    assert client.post("/opportunities", json=payload).status_code == 401
    assert client.post("/opportunities", json=payload, headers=auth()).status_code == 201


def test_missing_server_token_fails_closed(client, monkeypatch):
    monkeypatch.delenv("EARNORBIT_API_TOKEN")
    assert client.get("/summary").status_code == 503


def test_recommendations_require_verified_active_official_api(client):
    base = {"category": "affiliate", "platform_url": "https://example.com", "country_eligibility": "GLOBAL",
            "payout_method": "crypto", "official_api": True, "terms_verified": True, "status": "active"}
    for name, changes in [
        ("Approved", {}),
        ("Unverified", {"terms_verified": False}),
        ("No official API", {"official_api": False}),
        ("Paused", {"status": "pending"}),
    ]:
        payload = {"name": name, **base, **changes}
        response = client.post("/opportunities", json=payload, headers=auth())
        assert response.status_code == 201
    result = client.get("/opportunities/recommended?country=DE&crypto_only=true", headers=auth())
    assert result.status_code == 200
    assert [item["name"] for item in result.json()] == ["Approved"]


def test_unknown_country_is_not_assumed_global(client):
    payload = {"name": "Unknown Country", "category": "affiliate", "platform_url": "https://example.com",
               "country_eligibility": "unknown", "official_api": True, "terms_verified": True, "status": "active"}
    assert client.post("/opportunities", json=payload, headers=auth()).status_code == 201
    result = client.get("/opportunities/recommended?country=DE", headers=auth())
    assert result.status_code == 200
    assert result.json() == []
