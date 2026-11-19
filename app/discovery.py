from sqlmodel import Session, select
from .models import Opportunity


def recommend_opportunities(
    session: Session,
    country: str | None = None,
    crypto_only: bool = False,
    limit: int = 50,
):
    """
    Return only manually approved, active opportunities with verified terms
    and an official API. Unknown country eligibility is never treated as global.
    """
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

    def score(item):
        # Transparent quality score, not an earnings prediction.
        return (
            4 * bool(item.terms_verified)
            + 3 * bool(item.official_api)
            + 2 * ((item.payout_method or "").lower().find("crypto") >= 0)
            + 1 * ((item.country_eligibility or "").upper() == "GLOBAL")
        )

    eligible.sort(key=lambda item: (score(item), item.created_at), reverse=True)
    return eligible[:max(1, min(limit, 100))]
