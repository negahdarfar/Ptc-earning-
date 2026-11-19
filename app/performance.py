from collections import defaultdict
from decimal import Decimal, InvalidOperation

from sqlmodel import Session, select

from .models import WorkSession


def _amount(value: str) -> Decimal:
    try:
        amount = Decimal(value)
        return amount if amount.is_finite() and amount >= 0 else Decimal("0")
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0")


def build_performance_summary(session: Session):
    """Measure approved task value against all tracked time, without calling it cash."""
    rows = session.exec(select(WorkSession)).all()
    groups = defaultdict(lambda: {
        "minutes_spent": 0, "approved_value": Decimal("0"), "pending_value": Decimal("0"),
        "approved_count": 0, "rejected_count": 0, "pending_count": 0, "abandoned_count": 0,
    })
    for row in rows:
        key = (row.source_name, row.currency.upper())
        item = groups[key]
        item["minutes_spent"] += row.minutes_spent
        if row.status == "approved":
            item["approved_value"] += _amount(row.reward_amount)
            item["approved_count"] += 1
        elif row.status == "pending":
            item["pending_value"] += _amount(row.reward_amount)
            item["pending_count"] += 1
        elif row.status == "rejected":
            item["rejected_count"] += 1
        elif row.status == "abandoned":
            item["abandoned_count"] += 1

    output = []
    for (source, currency), item in groups.items():
        decided = item["approved_count"] + item["rejected_count"]
        hourly = item["approved_value"] * Decimal("60") / Decimal(item["minutes_spent"])
        output.append({
            "source_name": source,
            "currency": currency,
            "minutes_spent": item["minutes_spent"],
            "approved_value_not_cash": str(item["approved_value"].quantize(Decimal("0.01"))),
            "pending_value_not_cash": str(item["pending_value"].quantize(Decimal("0.01"))),
            "approved_value_per_tracked_hour": str(hourly.quantize(Decimal("0.01"))),
            "approval_rate_percent": str(
                (Decimal(item["approved_count"]) * Decimal("100") / Decimal(decided)).quantize(Decimal("0.01"))
                if decided else Decimal("0")
            ),
            "approved_tasks": item["approved_count"],
            "rejected_tasks": item["rejected_count"],
            "pending_tasks": item["pending_count"],
            "abandoned_tasks": item["abandoned_count"],
        })
    output.sort(key=lambda row: Decimal(row["approved_value_per_tracked_hour"]), reverse=True)
    return {
        "sources": output,
        "important": "Approved and pending task rewards are not cash received. This productivity view is separate from the confirmed revenue and paid-expense ledger.",
    }
