from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


def test_work_sessions_produce_source_level_performance_without_calling_rewards_cash(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    engine = create_engine(f"sqlite:///{tmp_path / 'performance.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    headers = {"Authorization": "Bearer test-secret-token"}
    try:
        with TestClient(app) as client:
            for payload in [
                {"source_name": "Task Site", "minutes_spent": 30, "reward_amount": "5", "currency": "USD", "status": "approved"},
                {"source_name": "Task Site", "minutes_spent": 30, "reward_amount": "0", "currency": "USD", "status": "rejected"},
                {"source_name": "Task Site", "minutes_spent": 15, "reward_amount": "2", "currency": "USD", "status": "pending"},
            ]:
                response = client.post("/work-sessions", headers=headers, json=payload)
                assert response.status_code == 201

            result = client.get("/performance", headers=headers)
            assert result.status_code == 200
            row = result.json()["sources"][0]
            assert row["minutes_spent"] == 75
            assert row["approved_value_not_cash"] == "5.00"
            assert row["pending_value_not_cash"] == "2.00"
            assert row["approved_value_per_tracked_hour"] == "4.00"
            assert row["approval_rate_percent"] == "50.00"
            assert "not cash received" in result.json()["important"]
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_work_session_rejects_reward_for_rejected_task(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    engine = create_engine(f"sqlite:///{tmp_path / 'performance-validation.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    try:
        with TestClient(app) as client:
            response = client.post("/work-sessions", headers={"Authorization": "Bearer test-secret-token"}, json={
                "source_name": "Task Site", "minutes_spent": 15, "reward_amount": "3", "status": "rejected",
            })
            assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
