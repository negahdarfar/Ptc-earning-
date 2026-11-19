"""Curated first-party discovery queue. These are leads, not eligibility claims."""
from sqlmodel import Session, select

from .models import SourceLead


INITIAL_SOURCE_LEADS = (
    {
        "platform_key": "upwork",
        "platform_name": "Upwork",
        "category": "client_services",
        "source_url": "https://www.upwork.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Start with manual workflow; API access requires separate provider approval.",
    },
    {
        "platform_key": "fiverr",
        "platform_name": "Fiverr",
        "category": "client_services",
        "source_url": "https://www.fiverr.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify current seller terms, payout methods and country rules.",
    },
    {
        "platform_key": "gumroad",
        "platform_name": "Gumroad",
        "category": "digital_product",
        "source_url": "https://gumroad.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify creator onboarding and country-specific payout coverage.",
    },
    {
        "platform_key": "amazon-associates",
        "platform_name": "Amazon Associates",
        "category": "affiliate",
        "source_url": "https://affiliate-program.amazon.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify the relevant local program, traffic rules and payout requirements.",
    },
    {
        "platform_key": "clickworker",
        "platform_name": "Clickworker",
        "category": "microtask",
        "source_url": "https://www.clickworker.com/",
        "source_type": "microtask",
        "review_notes": "Research lead only. Registration, task supply and payout options vary by country.",
    },
    {
        "platform_key": "prolific",
        "platform_name": "Prolific",
        "category": "research",
        "source_url": "https://www.prolific.com/",
        "source_type": "research",
        "review_notes": "Research lead only. Participation is limited to supported countries and account verification.",
    },
)


def seed_initial_source_leads(session: Session) -> int:
    """Insert missing curated leads without overwriting operator review decisions."""
    inserted = 0
    for item in INITIAL_SOURCE_LEADS:
        existing = session.exec(
            select(SourceLead).where(SourceLead.platform_key == item["platform_key"])
        ).first()
        if existing:
            continue
        session.add(SourceLead(**item))
        inserted += 1
    if inserted:
        session.commit()
    return inserted
