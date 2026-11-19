from calendar import monthrange
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from sqlmodel import Session, select

from .discovery import rank_opportunities
from .models import ExpenseEntry, RevenueEntry


def _amount(value: str) -> Decimal:
    try:
        amount = Decimal(value)
        return amount if amount.is_finite() and amount >= 0 else Decimal("0")
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0")


def build_optimizer_plan(
    session: Session,
    target: str = "1000",
    currency: str = "USD",
    hours_per_day: float = 2.0,
    country: str | None = None,
):
    """Calculate a transparent monthly gap and capacity plan; never forecast unverified cash."""
    now = datetime.now(timezone.utc)
    target_amount = _amount(target)
    currency_code = currency.strip().upper()
    days_in_month = monthrange(now.year, now.month)[1]
    days_remaining = max(1, days_in_month - now.day + 1)
    hours_remaining = Decimal(str(hours_per_day)) * Decimal(days_remaining)

    revenue = session.exec(select(RevenueEntry)).all()
    expenses = session.exec(select(ExpenseEntry)).all()
    confirmed = sum(
        (_amount(row.amount) for row in revenue
         if row.status == "confirmed" and row.currency.upper() == currency_code
         and row.recorded_at.year == now.year and row.recorded_at.month == now.month),
        Decimal("0"),
    )
    paid_costs = sum(
        (_amount(row.amount) for row in expenses
         if row.status == "paid" and row.currency.upper() == currency_code
         and row.recorded_at.year == now.year and row.recorded_at.month == now.month),
        Decimal("0"),
    )
    net_actual = confirmed - paid_costs
    gap = max(Decimal("0"), target_amount - net_actual)
    daily_required = gap / Decimal(days_remaining)
    hourly_required = gap / hours_remaining if hours_remaining > 0 else gap

    ranked = rank_opportunities(session, country=country, limit=100)
    # With no operator-selected country, only explicitly GLOBAL opportunities are eligible.
    eligible = [
        row for row in ranked
        if row["country_eligibility"] == "GLOBAL"
        or (country and row["country_eligibility"] == country.strip().upper())
    ]
    eligible = [row for row in eligible if row["payout_currency"].strip().upper() == currency_code]
    sources = []
    for row in eligible[:10]:
        rate = Decimal(row["risk_adjusted_net_hourly"]) if row["risk_adjusted_net_hourly"] is not None else Decimal("0")
        sources.append({
            "opportunity_id": row["opportunity_id"],
            "name": row["name"],
            "category": row["category"],
            "risk_adjusted_net_hourly": str(rate.quantize(Decimal("0.01"))),
            "currency": currency_code,
            "confidence_score": row["confidence_score"],
            "freshness_status": row["freshness_status"],
            "hours_to_cover_current_gap_at_this_rate": (
                str((gap / rate).quantize(Decimal("0.1"))) if rate > 0 else None
            ),
            "economics_status": "estimate_only_not_income",
        })

    best_rate = max(
        (Decimal(row["risk_adjusted_net_hourly"]) for row in eligible if row["risk_adjusted_net_hourly"] is not None),
        default=Decimal("0"),
    )
    if gap == 0:
        assessment = "monthly_target_reached_on_recorded_net"
    elif best_rate == 0:
        assessment = "insufficient_verified_opportunity_data"
    elif best_rate < hourly_required:
        assessment = "stretch_target_at_current_time_capacity"
    else:
        assessment = "mathematically_within_estimated_capacity_not_guaranteed"

    return {
        "period": now.strftime("%Y-%m"),
        "currency": currency_code,
        "monthly_target": str(target_amount),
        "confirmed_revenue_this_month": str(confirmed),
        "paid_expenses_this_month": str(paid_costs),
        "actual_net_this_month": str(net_actual),
        "remaining_gap": str(gap.quantize(Decimal("0.01"))),
        "days_remaining_including_today": days_remaining,
        "available_hours_per_day_assumption": str(hours_per_day),
        "remaining_capacity_hours": str(hours_remaining.quantize(Decimal("0.1"))),
        "required_net_per_day": str(daily_required.quantize(Decimal("0.01"))),
        "required_net_per_available_hour": str(hourly_required.quantize(Decimal("0.01"))),
        "best_confidence_adjusted_hourly_estimate": str(best_rate.quantize(Decimal("0.01"))),
        "assessment": assessment,
        "eligible_sources": sources,
        "important": "This is a planning model, not a promise. Estimates are not income; only confirmed revenue minus paid costs is actual net. Unknown country eligibility is excluded unless the source explicitly says GLOBAL.",
    }
