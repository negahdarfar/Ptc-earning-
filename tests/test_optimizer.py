from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


def test_optimizer_reports_real_gap_and_excludes_unknown_eligibility(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    engine = create_engine(f"sqlite:///{tmp_path / 'optimizer.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    headers = {"Authorization": "Bearer test-secret-token"}
    try:
        with TestClient(app) as client:
            now = datetime.now(timezone.utc).isoformat()
            for name, scope in [("Global Source", "GLOBAL"), ("Unknown Source", "unknown")]:
                created = client.post("/opportunities", headers=headers, json={
                    "name": name, "category": "microtask", "platform_url": "https://example.com",
                    "status": "active", "terms_verified": True,
                })
                assert created.status_code == 201
                opportunity_id = created.json()["id"]
                evidence = client.post(f"/opportunities/{opportunity_id}/evidence", headers=headers, json={
                    "evidence_url": "https://example.com/terms", "reviewed_on": now,
                    "country_eligibility": scope, "kyc_summary": "As required by provider",
                    "payout_method": "bank transfer", "payout_currency": "USD",
                    "minimum_payout": "10 USD", "payout_fee_percent": "5",
                    "average_reward": "2", "estimated_task_minutes": "10",
                    "approval_rate_percent": "80",
                })
                assert evidence.status_code == 201

            result = client.get("/optimizer/plan?target=1000&currency=USD&hours_per_day=2", headers=headers)
            assert result.status_code == 200
            body = result.json()
            assert body["currency"] == "USD"
            assert body["monthly_target"] == "1000"
            assert body["remaining_gap"] == "1000.00"
            assert body["assessment"] in {
                "stretch_target_at_current_time_capacity",
                "mathematically_within_estimated_capacity_not_guaranteed",
            }
            assert [item["name"] for item in body["eligible_sources"]] == ["Global Source"]
            assert body["eligible_sources"][0]["risk_adjusted_net_hourly"] == "9.12"
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_optimizer_requires_auth(monkeypatch, tmp_path):
    monkeypatch.setenv("EARNORBIT_API_TOKEN", "test-secret-token")
    engine = create_engine(f"sqlite:///{tmp_path / 'optimizer-auth.db'}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    try:
        with TestClient(app) as client:
            assert client.get("/optimizer/plan").status_code == 401
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
