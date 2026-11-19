import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Opportunity, RevenueEntry, ExpenseEntry, DigitalProduct, OpportunityEvidence, AuditEvent
from .schemas import (
    OpportunityCreate, OpportunityRead, RevenueCreate, RevenueRead,
    ExpenseCreate, ExpenseRead, DigitalProductCreate, DigitalProductRead,\n    OpportunityEvidenceCreate, OpportunityEvidenceRead,
)
from .services import (
    list_opportunities, list_revenue, list_expenses, build_summary,
    list_catalog_opportunities,
)
from .discovery import recommend_opportunities, rank_opportunities


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENVIRONMENT", "development").lower() == "production" and not os.getenv("EARNORBIT_API_TOKEN"):
        raise RuntimeError("EARNORBIT_API_TOKEN must be configured in production.")
    create_db_and_tables()
    yield


app = FastAPI(
    title=os.getenv("APP_NAME", "EarnOrbit"),
    description="A modular tracker for legitimate online earning opportunities, expenses, and verified net revenue.",
    version="0.3.0",
    lifespan=lifespan,
)


def require_api_token(authorization: str | None = Header(default=None)):
    expected = os.getenv("EARNORBIT_API_TOKEN", "")
    if not expected:
        raise HTTPException(status_code=503, detail="API authentication is not configured.")
    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not supplied or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="A valid Bearer token is required.", headers={"WWW-Authenticate": "Bearer"})
    return True


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/")
def root():
    return {"name": "EarnOrbit", "version": "0.3.0", "docs": "/docs", "dashboard": "/dashboard", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "earnorbit"}


@app.post("/opportunities", response_model=OpportunityRead, status_code=201, dependencies=[Depends(require_api_token)])
def create_opportunity(payload: OpportunityCreate, session: Session = Depends(get_session)):
    item = Opportunity(**payload.model_dump(mode="json"))
    item.platform_url = str(payload.platform_url)
    session.add(item)
    session.flush()
    session.add(AuditEvent(event_type="opportunity_created", entity_type="opportunity", entity_id=item.id,
                           details="Opportunity intake record created."))
    session.commit()
    session.refresh(item)
    return item


@app.get("/opportunities", response_model=list[OpportunityRead], dependencies=[Depends(require_api_token)])
def get_opportunities(status: str | None = Query(default=None), category: str | None = Query(default=None, min_length=2, max_length=60), session: Session = Depends(get_session)):
    return list_opportunities(session, status, category)


@app.get("/opportunities/catalog", response_model=list[OpportunityRead], dependencies=[Depends(require_api_token)])
def get_opportunity_catalog(category: str | None = Query(default=None, min_length=2, max_length=60), limit: int = Query(default=100, ge=1, le=250), session: Session = Depends(get_session)):
    """Reviewed catalog for manual and API-enabled sources; listing never authorizes automated activity."""
    return list_catalog_opportunities(session, category, limit)



@app.post("/opportunities/{opportunity_id}/evidence", response_model=OpportunityEvidenceRead, status_code=201, dependencies=[Depends(require_api_token)])
def add_opportunity_evidence(opportunity_id: int, payload: OpportunityEvidenceCreate, session: Session = Depends(get_session)):
    opportunity = session.get(Opportunity, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    if payload.reviewed_on.date().isoformat() > __import__("datetime").date.today().isoformat():
        raise HTTPException(status_code=422, detail="reviewed_on cannot be in the future")
    fee, reward, minutes, approval = map(float, (payload.payout_fee_percent, payload.average_reward, payload.estimated_task_minutes, payload.approval_rate_percent))
    if fee > 100 or approval > 100:
        raise HTTPException(status_code=422, detail="fee and approval rate must be between 0 and 100")
    if reward > 0 and minutes <= 0:
        raise HTTPException(status_code=422, detail="task minutes must be positive when reward is supplied")
    evidence = OpportunityEvidence(opportunity_id=opportunity_id, **payload.model_dump(mode="json"))
    evidence.evidence_url = str(payload.evidence_url)
    session.add(evidence)
    opportunity.country_eligibility = payload.country_eligibility
    opportunity.payout_method = payload.payout_method
    opportunity.payout_currency = payload.payout_currency
    opportunity.minimum_payout = payload.minimum_payout
    opportunity.terms_verified = True
    session.add(AuditEvent(event_type="evidence_added", entity_type="opportunity", entity_id=opportunity_id,
                           details="Dated evidence and unit-economics inputs recorded."))
    session.add(opportunity)
    session.commit()
    session.refresh(evidence)
    return evidence


@app.get("/opportunities/{opportunity_id}/evidence", response_model=list[OpportunityEvidenceRead], dependencies=[Depends(require_api_token)])
def get_opportunity_evidence(opportunity_id: int, session: Session = Depends(get_session)):
    if not session.get(Opportunity, opportunity_id):
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return session.exec(select(OpportunityEvidence).where(OpportunityEvidence.opportunity_id == opportunity_id)
                        .order_by(OpportunityEvidence.reviewed_on.desc())).all()


@app.get("/opportunities/ranked", dependencies=[Depends(require_api_token)])
def get_ranked_opportunities(country: str | None = Query(default=None, min_length=2, max_length=2),
                             category: str | None = Query(default=None, min_length=2, max_length=60),
                             limit: int = Query(default=50, ge=1, le=100),
                             session: Session = Depends(get_session)):
    return rank_opportunities(session, country=country, category=category, limit=limit)


@app.post("/products", response_model=DigitalProductRead, status_code=201, dependencies=[Depends(require_api_token)])
def create_product(payload: DigitalProductCreate, session: Session = Depends(get_session)):
    if payload.status not in {"draft", "ready", "archived"}:
        raise HTTPException(status_code=422, detail="status must be draft, ready, or archived")
    if payload.status == "ready" and (not payload.rights_confirmed or not payload.asset_url):
        raise HTTPException(status_code=422, detail="ready products require confirmed rights and an asset URL")
    item = DigitalProduct(**payload.model_dump(mode="json"))
    item.asset_url = str(payload.asset_url) if payload.asset_url else None
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/products", response_model=list[DigitalProductRead], dependencies=[Depends(require_api_token)])
def get_products(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    statement = select(DigitalProduct).order_by(DigitalProduct.created_at.desc())
    if status:
        if status not in {"draft", "ready", "archived"}:
            raise HTTPException(status_code=422, detail="invalid product status")
        statement = statement.where(DigitalProduct.status == status)
    return session.exec(statement).all()


@app.post("/revenue", response_model=RevenueRead, status_code=201, dependencies=[Depends(require_api_token)])
def create_revenue(payload: RevenueCreate, session: Session = Depends(get_session)):
    if payload.status not in {"pending", "confirmed", "rejected"}:
        raise HTTPException(status_code=422, detail="status must be pending, confirmed, or rejected")
    entry = RevenueEntry(**payload.model_dump())
    session.add(entry)
    session.flush()
    session.add(AuditEvent(event_type="revenue_recorded", entity_type="revenue", entity_id=entry.id,
                           details="Revenue ledger entry created; confirmation status is tracked separately."))
    session.commit()
    session.refresh(entry)
    return entry


@app.get("/revenue", response_model=list[RevenueRead], dependencies=[Depends(require_api_token)])
def get_revenue(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    return list_revenue(session, status)


@app.post("/expenses", response_model=ExpenseRead, status_code=201, dependencies=[Depends(require_api_token)])
def create_expense(payload: ExpenseCreate, session: Session = Depends(get_session)):
    if payload.status not in {"planned", "paid", "void"}:
        raise HTTPException(status_code=422, detail="status must be planned, paid, or void")
    entry = ExpenseEntry(**payload.model_dump())
    session.add(entry)
    session.flush()
    session.add(AuditEvent(event_type="expense_recorded", entity_type="expense", entity_id=entry.id,
                           details="Expense ledger entry created."))
    session.commit()
    session.refresh(entry)
    return entry


@app.get("/expenses", response_model=list[ExpenseRead], dependencies=[Depends(require_api_token)])
def get_expenses(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    if status and status not in {"planned", "paid", "void"}:
        raise HTTPException(status_code=422, detail="invalid expense status")
    return list_expenses(session, status)


@app.get("/opportunities/recommended", response_model=list[OpportunityRead], dependencies=[Depends(require_api_token)])
def get_recommended_opportunities(country: str | None = Query(default=None, min_length=2, max_length=2), crypto_only: bool = False, limit: int = Query(default=50, ge=1, le=100), session: Session = Depends(get_session)):
    return recommend_opportunities(session, country, crypto_only, limit)


@app.get("/audit", dependencies=[Depends(require_api_token)])
def get_audit_events(limit: int = Query(default=100, ge=1, le=500), session: Session = Depends(get_session)):
    """Read recent audit events; sensitive payloads and credentials are never logged."""
    return session.exec(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit)).all()


@app.get("/summary", dependencies=[Depends(require_api_token)])
def summary(session: Session = Depends(get_session)):
    return build_summary(session)
