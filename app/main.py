import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query\nfrom fastapi.responses import FileResponse\nfrom pathlib import Path
from sqlmodel import Session
from .database import create_db_and_tables, get_session
from .models import Opportunity, RevenueEntry
from .schemas import OpportunityCreate, OpportunityRead, RevenueCreate, RevenueRead
from .services import list_opportunities, list_revenue, build_summary

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title=os.getenv("APP_NAME", "EarnOrbit"),
    description="A modular tracker for legitimate online earning opportunities and confirmed revenue.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"name": "EarnOrbit", "version": "0.1.0", "docs": "/docs", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "earnorbit"}

@app.post("/opportunities", response_model=OpportunityRead, status_code=201)
def create_opportunity(payload: OpportunityCreate, session: Session = Depends(get_session)):
    item = Opportunity(**payload.model_dump(mode="json"))
    item.platform_url = str(payload.platform_url)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/opportunities", response_model=list[OpportunityRead])
def get_opportunities(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    return list_opportunities(session, status)

@app.post("/revenue", response_model=RevenueRead, status_code=201)
def create_revenue(payload: RevenueCreate, session: Session = Depends(get_session)):
    if payload.status not in {"pending", "confirmed", "rejected"}:
        raise HTTPException(status_code=422, detail="status must be pending, confirmed, or rejected")
    entry = RevenueEntry(**payload.model_dump())
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@app.get("/revenue", response_model=list[RevenueRead])
def get_revenue(status: str | None = Query(default=None), session: Session = Depends(get_session)):
    return list_revenue(session, status)

@app.get("/summary")
def summary(session: Session = Depends(get_session)):
    return build_summary(session)
