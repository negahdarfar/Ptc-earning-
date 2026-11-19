from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

from sqlmodel import Session, select

from .models import Opportunity, OpportunityEvidence


def recommend_opportunities(session: Session, country: str | None = None, crypto_only: bool = False, limit: int = 50):
    """Conservative recommendation list; unknown eligibility is not assumed global."""
    statement = select(Opportunity).where(
        Opportunity.status == "active",
        Opportunity.terms_verified.is_(True),
        Opportunity.official_api.is_(True),
    )
    if crypto_only:
        statement = statement.where(Opportunity.payout_method.ilike("%crypto%"))
    candidates = session.exec(statement).all()
    country_code = country.strip().upper() if country else None
    eligible = []
    for item in candidates:
        eligibility = (item.country_eligibility or "unknown").strip().upper()
        if country_code and eligibility not in {"GLOBAL", country_code}:
            continue
        eligible.append(item)
    eligible.sort(key=lambda item: (
        4 * bool(item.terms_verified) + 3 * bool(item.official_api)
        + 2 * ("crypto" in (item.payout_method or "").lower())
        + 1 * ((item.country_eligibility or "").upper() == "GLOBAL"),
        item.created_at
    ), reverse=True)
    return eligible[:max(1, min(limit, 100))]


def _d(value: str) -> Decimal | None:
    try:
        result = Decimal(value)
        return result if result.is_finite() and result >= 0 else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def _evidence_age_days(value: str, today: date) -> int:
    try:
        reviewed = datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
        return max(0, (today - reviewed).days)
    except (TypeError, ValueError):
        try:
            return max(0, (today - date.fromisoformat(str(value)[:10])).days)
        except (TypeError, ValueError):
            return 365


def rank_opportunities(session: Session, country: str | None = None, category: str | None = None, limit: int = 50):
    """Rank evidence-backed opportunities by confidence-adjusted net hourly yield."""
    statement = select(Opportunity).where(Opportunity.terms_verified.is_(True))
    if category:
        statement = statement.where(Opportunity.category.ilike(category.strip()))
    opportunities = session.exec(statement).all()
    output = []
    today = datetime.now(timezone.utc).date()
    for item in opportunities:
        evidence_rows = session.exec(
            select(OpportunityEvidence)
            .where(OpportunityEvidence.opportunity_id == item.id)
            .order_by(OpportunityEvidence.reviewed_on.desc(), OpportunityEvidence.id.desc())
        ).all()
        if not evidence_rows:
            continue
        evidence = evidence_rows[0]
        eligible = (evidence.country_eligibility or "unknown").strip().upper()
        if country and eligible not in {"GLOBAL", country.strip().upper()}:
            continue

        reward = _d(evidence.average_reward)
        fee = _d(evidence.payout_fee_percent)
        minutes = _d(evidence.estimated_task_minutes)
        approval = _d(evidence.approval_rate_percent)
        if None in (reward, fee, minutes, approval) or minutes == 0 or fee > 100 or approval > 100:
            hourly = None
        else:
            hourly = (
                reward * (Decimal("1") - fee / Decimal("100"))
                * approval / Decimal("100") * Decimal("60") / minutes
            )

        age_days = _evidence_age_days(evidence.reviewed_on, today)
        known_fields = sum([
            bool(evidence.evidence_url and evidence.evidence_url.startswith("https://")),
            bool(eligible not in {"", "UNKNOWN", "UNKNOWN/UNVERIFIED"}),
            bool(evidence.kyc_summary and evidence.kyc_summary.lower() != "unknown"),
            bool(evidence.payout_method and evidence.payout_method.lower() != "unknown"),
            bool(evidence.payout_currency and evidence.payout_currency.lower() != "unknown"),
            bool(evidence.minimum_payout and evidence.minimum_payout.lower() != "unknown"),
        ])
        freshness_factor = max(Decimal("0"), Decimal("1") - Decimal(age_days) / Decimal("365"))
        confidence = (Decimal(known_fields) / Decimal("6") * freshness_factor * Decimal("100"))
        risk_adjusted = hourly * confidence / Decimal("100") if hourly is not None else None
        freshness_status = "fresh" if age_days <= 30 else "review_due" if age_days <= 90 else "stale"

        output.append({
            "opportunity_id": item.id,
            "name": item.name,
            "category": item.category,
            "platform_url": item.platform_url,
            "status": item.status,
            "country_eligibility": eligible,
            "kyc_summary": evidence.kyc_summary,
            "payout_method": evidence.payout_method,
            "payout_currency": evidence.payout_currency,
            "minimum_payout": evidence.minimum_payout,
            "evidence_url": evidence.evidence_url,
            "reviewed_on": evidence.reviewed_on,
            "evidence_age_days": age_days,
            "freshness_status": freshness_status,
            "confidence_score": str(confidence.quantize(Decimal("0.01"))),
            "estimated_net_hourly": str(hourly.quantize(Decimal("0.01"))) if hourly is not None else None,
            "risk_adjusted_net_hourly": str(risk_adjusted.quantize(Decimal("0.01"))) if risk_adjusted is not None else None,
            "economics_status": "estimated_not_verified",
            "approval_rate_percent": evidence.approval_rate_percent,
            "estimated_task_minutes": evidence.estimated_task_minutes,
        })
    output.sort(key=lambda row: (
        Decimal(row["risk_adjusted_net_hourly"]) if row["risk_adjusted_net_hourly"] is not None else Decimal("-1"),
        Decimal(row["estimated_net_hourly"]) if row["estimated_net_hourly"] is not None else Decimal("-1"),
    ), reverse=True)
    return output[:max(1, min(limit, 100))]
