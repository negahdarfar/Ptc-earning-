from decimal import Decimal, InvalidOperation
from sqlmodel import Session, select
from .models import Opportunity, RevenueEntry

def list_opportunities(session: Session, status: str | None = None):
    statement = select(Opportunity).order_by(Opportunity.created_at.desc())
    if status:
        statement = statement.where(Opportunity.status == status)
    return session.exec(statement).all()

def list_revenue(session: Session, status: str | None = None):
    statement = select(RevenueEntry).order_by(RevenueEntry.recorded_at.desc())
    if status:
        statement = statement.where(RevenueEntry.status == status)
    return session.exec(statement).all()

def build_summary(session: Session):
    entries = session.exec(select(RevenueEntry)).all()
    totals: dict[str, Decimal] = {}
    confirmed_count = pending_count = 0
    for entry in entries:
        if entry.status == "confirmed":
            try:
                totals[entry.currency] = totals.get(entry.currency, Decimal("0")) + Decimal(entry.amount)
                confirmed_count += 1
            except InvalidOperation:
                continue
        elif entry.status == "pending":
            pending_count += 1
    return {
        "confirmed_revenue_by_currency": {k: str(v) for k, v in totals.items()},
        "confirmed_entries": confirmed_count,
        "pending_entries": pending_count,
        "note": "Confirmed revenue only; expenses and payout fees are not yet modeled."
    }
