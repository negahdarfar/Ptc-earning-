from decimal import Decimal, InvalidOperation
from sqlmodel import Session, select
from .models import Opportunity, RevenueEntry, ExpenseEntry

def list_opportunities(session: Session, status: str | None = None, category: str | None = None):
    statement = select(Opportunity).order_by(Opportunity.created_at.desc())
    if status:
        statement = statement.where(Opportunity.status == status)
    if category:
        statement = statement.where(Opportunity.category.ilike(category.strip()))
    return session.exec(statement).all()


def list_catalog_opportunities(session: Session, category: str | None = None, limit: int = 100):
    """Return human-reviewed active sources; this does not authorize automated activity."""
    statement = select(Opportunity).where(
        Opportunity.status == "active",
        Opportunity.terms_verified.is_(True),
    ).order_by(Opportunity.created_at.desc())
    if category:
        statement = statement.where(Opportunity.category.ilike(category.strip()))
    return session.exec(statement.limit(max(1, min(limit, 250)))).all()


def list_revenue(session: Session, status: str | None = None):
    statement = select(RevenueEntry).order_by(RevenueEntry.recorded_at.desc())
    if status:
        statement = statement.where(RevenueEntry.status == status)
    return session.exec(statement).all()


def list_expenses(session: Session, status: str | None = None):
    statement = select(ExpenseEntry).order_by(ExpenseEntry.recorded_at.desc())
    if status:
        statement = statement.where(ExpenseEntry.status == status)
    return session.exec(statement).all()


def _decimal(value: str) -> Decimal | None:
    try:
        amount = Decimal(value)
        return amount if amount.is_finite() and amount >= 0 else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def build_summary(session: Session):
    revenue = session.exec(select(RevenueEntry)).all()
    expenses = session.exec(select(ExpenseEntry)).all()
    gross: dict[str, Decimal] = {}
    costs: dict[str, Decimal] = {}
    confirmed_count = pending_count = paid_expense_count = 0

    for entry in revenue:
        if entry.status == "confirmed":
            amount = _decimal(entry.amount)
            if amount is not None:
                gross[entry.currency] = gross.get(entry.currency, Decimal("0")) + amount
                confirmed_count += 1
        elif entry.status == "pending":
            pending_count += 1

    for entry in expenses:
        if entry.status == "paid":
            amount = _decimal(entry.amount)
            if amount is not None:
                costs[entry.currency] = costs.get(entry.currency, Decimal("0")) + amount
                paid_expense_count += 1

    currencies = sorted(set(gross) | set(costs))
    net = {currency: gross.get(currency, Decimal("0")) - costs.get(currency, Decimal("0")) for currency in currencies}
    return {
        "confirmed_revenue_by_currency": {k: str(v) for k, v in gross.items()},
        "paid_expenses_by_currency": {k: str(v) for k, v in costs.items()},
        "net_profit_by_currency": {k: str(v) for k, v in net.items()},
        "confirmed_entries": confirmed_count,
        "pending_entries": pending_count,
        "paid_expense_entries": paid_expense_count,
        "monthly_target": {"amount": "1000", "currency": "USD", "status": "aspirational_not_guaranteed"},
        "note": "Net is calculated only within each currency; no FX conversion, unpaid costs, taxes, or payout fees are inferred."
    }
