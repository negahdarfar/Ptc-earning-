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


def test_product_catalog_requires_auth(client):
    assert client.get("/products").status_code == 401
    assert client.post("/products", json={"title": "Useful Template", "category": "template",
        "short_description": "A useful downloadable template."}).status_code == 401


def test_create_and_list_digital_product_draft(client):
    payload = {"title": "Trading Journal Template", "category": "template", "language": "en",
        "short_description": "A structured journal for reviewing trades.",
        "full_description": "Editable spreadsheet template for personal trade reviews.",
        "price_amount": "9.99", "price_currency": "USD", "status": "draft"}
    created = client.post("/products", json=payload, headers=auth())
    assert created.status_code == 201
    assert created.json()["title"] == payload["title"]
    listed = client.get("/products?status=draft", headers=auth())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_ready_product_requires_rights_and_asset_url(client):
    payload = {"title": "Original Guide", "category": "ebook",
        "short_description": "An original guide for learning.",
        "status": "ready", "rights_confirmed": False,
        "asset_url": "https://example.com/file.pdf"}
    assert client.post("/products", json=payload, headers=auth()).status_code == 422
    payload["rights_confirmed"] = True
    assert client.post("/products", json=payload, headers=auth()).status_code == 201


def test_product_price_must_be_numeric(client):
    payload = {"title": "Useful Template", "category": "template",
        "short_description": "A useful downloadable template.", "price_amount": "nine"}
    assert client.post("/products", json=payload, headers=auth()).status_code == 422



def test_opportunity_catalog_includes_reviewed_manual_sources_but_not_unreviewed(client):
    base = {"category": "ptc", "platform_url": "https://example.com",
            "country_eligibility": "unknown", "official_api": False,
            "terms_verified": True, "status": "active"}
    assert client.post("/opportunities", json={"name": "Manual PTC", **base}, headers=auth()).status_code == 201
    unreviewed = {**base, "name": "Unreviewed PTC", "terms_verified": False}
    assert client.post("/opportunities", json=unreviewed, headers=auth()).status_code == 201
    result = client.get("/opportunities/catalog?category=ptc", headers=auth())
    assert [item["name"] for item in result.json()] == ["Manual PTC"]
    assert client.get("/opportunities/catalog", headers=auth()).status_code == 200
    assert client.get("/opportunities/catalog").status_code == 401


def test_opportunity_category_filter(client):
    for name, category in [("PTC One", "ptc"), ("Task One", "microtask")]:
        payload = {"name": name, "category": category, "platform_url": "https://example.com"}
        assert client.post("/opportunities", json=payload, headers=auth()).status_code == 201
    result = client.get("/opportunities?category=ptc", headers=auth())
    assert [item["name"] for item in result.json()] == ["PTC One"]


def test_expense_ledger_requires_auth_and_tracks_paid_costs(client):
    payload = {"source_name": "Hosting", "amount": "12.50", "currency": "USD", "status": "paid"}
    assert client.post("/expenses", json=payload).status_code == 401
    created = client.post("/expenses", json=payload, headers=auth())
    assert created.status_code == 201
    assert created.json()["amount"] == "12.50"
    assert client.get("/expenses", headers=auth()).status_code == 200


def test_summary_reports_net_by_currency_without_mixing_currencies(client):
    revenue = [
        {"source_name": "Task platform", "amount": "100.00", "currency": "USD", "status": "confirmed"},
        {"source_name": "Survey platform", "amount": "50.00", "currency": "EUR", "status": "confirmed"},
        {"source_name": "Pending task", "amount": "900.00", "currency": "USD", "status": "pending"},
    ]
    for item in revenue:
        assert client.post("/revenue", json=item, headers=auth()).status_code == 201
    expenses = [
        {"source_name": "Hosting", "amount": "12.50", "currency": "USD", "status": "paid"},
        {"source_name": "Tool", "amount": "10.00", "currency": "EUR", "status": "paid"},
        {"source_name": "Planned subscription", "amount": "5.00", "currency": "USD", "status": "planned"},
    ]
    for item in expenses:
        assert client.post("/expenses", json=item, headers=auth()).status_code == 201

    result = client.get("/summary", headers=auth())
    assert result.status_code == 200
    data = result.json()
    assert data["confirmed_revenue_by_currency"] == {"USD": "100.00", "EUR": "50.00"}
    assert data["paid_expenses_by_currency"] == {"USD": "12.50", "EUR": "10.00"}
    assert data["net_profit_by_currency"] == {"EUR": "40.00", "USD": "87.50"}
    assert data["pending_entries"] == 1
    assert data["monthly_target"] == {"amount": "1000", "currency": "USD", "status": "aspirational_not_guaranteed"}


def test_expense_rejects_invalid_status(client):
    payload = {"source_name": "Hosting", "amount": "12", "currency": "USD", "status": "confirmed"}
    assert client.post("/expenses", json=payload, headers=auth()).status_code == 422


def test_opportunity_evidence_and_ranked_unit_economics(client):
    created = client.post("/opportunities", json={"name":"Task Platform","category":"microtask","platform_url":"https://example.com"}, headers=auth())
    assert created.status_code == 201
    oid = created.json()["id"]
    evidence = {"evidence_url":"https://example.com/terms","reviewed_on":"2026-11-19T00:00:00",
        "country_eligibility":"GLOBAL","kyc_summary":"Identity verification may be required",
        "payout_method":"PayPal","payout_currency":"USD","minimum_payout":"10",
        "payout_fee_percent":"5","average_reward":"2","estimated_task_minutes":"10",
        "approval_rate_percent":"80","reviewer_notes":"Test evidence record"}
    saved = client.post(f"/opportunities/{oid}/evidence", json=evidence, headers=auth())
    assert saved.status_code == 201
    ranked = client.get("/opportunities/ranked?country=DE", headers=auth())
    assert ranked.status_code == 200
    assert ranked.json()[0]["estimated_net_hourly"] == "9.12"
    assert ranked.json()[0]["economics_status"] == "estimated_not_verified"
    assert client.get(f"/opportunities/{oid}/evidence").status_code == 401


def test_evidence_rejects_invalid_fee_and_missing_opportunity(client):
    evidence = {"evidence_url":"https://example.com/terms","reviewed_on":"2026-11-19T00:00:00","payout_fee_percent":"150"}
    assert client.post("/opportunities/999/evidence", json=evidence, headers=auth()).status_code == 404
    created = client.post("/opportunities", json={"name":"Sample","category":"ptc","platform_url":"https://example.com"}, headers=auth())
    assert created.status_code == 201
    assert client.post(f"/opportunities/{created.json()['id']}/evidence", json=evidence, headers=auth()).status_code == 422


def test_ranked_endpoint_and_audit_log_require_auth(client):
    assert client.get("/opportunities/ranked").status_code == 401
    assert client.get("/audit").status_code == 401
    created = client.post("/opportunities", json={"name":"Audit Source","category":"ptc","platform_url":"https://example.com"}, headers=auth())
    assert created.status_code == 201
    events = client.get("/audit", headers=auth())
    assert events.status_code == 200
    assert any(event["event_type"] == "opportunity_created" for event in events.json())
