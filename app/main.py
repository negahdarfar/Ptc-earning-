import os
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Opportunity, RevenueEntry, DigitalProduct
from .schemas import OpportunityCreate, OpportunityRead, RevenueCreate, RevenueRead, DigitalProductCreate, DigitalProductRead
from .services import list_opportunities, list_revenue, build_summary
from .discovery import recommend_opportunities


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("ENVIRONMENT", "development").lower() == "production" and not os.getenv("EARNORBIT_API_TOKEN"):
        raise RuntimeError("EARNORBIT_API_TOKEN must be configured in production.")
    create_db_and_tables()
    yield


app = FastAPI(
    title=os.getenv("APP_NAME", "EarnOrbit"),
    description="A modular tracker for legitimate online earning opportunities and confirmed revenue.",
    version="0.2.0",
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
    # The shell is public; all dashboard data and write APIs require the bearer token.
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/")
def root():
    return {"name": "EarnOrbit", "version": "0.2.0", "docs": "/docs", "dashboard": "/dashboard", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "earnorbit"}


@app.post("/opportunities", response_model=OpportunityRead, status_code=201, dependencies=[Depends(require_api_token)])
def create_opportunity(payload: OpportunityCreate, session: Session = Depends(get_session)):
    item = Opportunity(**payload.model_dump(mode="json"))
    item.platform_url = str(payload.platform_url)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/opportunities", response_model=list[OpportunityRead], dependencies=[Depends(require_api_token)])
def get_opportunities(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    return list_opportunities(session, status)


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
    session.commit()
    session.refresh(entry)
    return entry


@app.get("/opportunities/recommended", response_model=list[OpportunityRead], dependencies=[Depends(require_api_token)])
def get_recommended_opportunities(country: str | None = Query(default=None, min_length=2, max_length=2), crypto_only: bool = False, limit: int = Query(default=50, ge=1, le=100), session: Session = Depends(get_session)):
    return recommend_opportunities(session, country, crypto_only, limit)


@app.get("/revenue", response_model=list[RevenueRead], dependencies=[Depends(require_api_token)])
def get_revenue(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    return list_revenue(session, status)


@app.get("/summary", dependencies=[Depends(require_api_token)])
def summary(session: Session = Depends(get_session)):
    return build_summary(session)
