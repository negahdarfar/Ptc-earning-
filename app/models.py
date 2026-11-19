from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Opportunity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)
    platform_url: str
    country_eligibility: str = "unknown"
    payout_method: str = "unknown"
    payout_currency: str = "USD"
    minimum_payout: str = "unknown"
    estimated_rate: str = "unknown"
    official_api: bool = False
    terms_verified: bool = False
    status: str = Field(default="pending", index=True)
    notes: str = ""
    created_at: datetime = Field(default_factory=utc_now)

class RevenueEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_name: str = Field(index=True)
    amount: str
    currency: str = Field(default="USD", index=True)
    status: str = Field(default="pending", index=True)
    payout_reference: str = ""
    notes: str = ""
    recorded_at: datetime = Field(default_factory=utc_now)

class ExpenseEntry(SQLModel, table=True):
    """Track real operating costs separately from revenue."""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_name: str = Field(index=True)
    amount: str
    currency: str = Field(default="USD", index=True)
    status: str = Field(default="paid", index=True)
    notes: str = ""
    recorded_at: datetime = Field(default_factory=utc_now)

class DigitalProduct(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=160)
    category: str = Field(index=True, max_length=60)
    language: str = Field(default="en", max_length=12)
    short_description: str = Field(max_length=500)
    full_description: str = ""
    price_amount: str = "0"
    price_currency: str = "USD"
    asset_url: Optional[str] = None
    rights_confirmed: bool = False
    status: str = Field(default="draft", index=True)
    created_at: datetime = Field(default_factory=utc_now)


class OpportunityEvidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: int = Field(index=True, foreign_key="opportunity.id")
    evidence_url: str
    reviewed_on: str = Field(index=True)
    country_eligibility: str = "unknown"
    kyc_summary: str = "unknown"
    payout_method: str = "unknown"
    payout_currency: str = "USD"
    minimum_payout: str = "unknown"
    payout_fee_percent: str = "0"
    average_reward: str = "0"
    estimated_task_minutes: str = "0"
    approval_rate_percent: str = "0"
    reviewer_notes: str = ""
    created_at: datetime = Field(default_factory=utc_now)


class AuditEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(index=True)
    entity_type: str = Field(index=True)
    entity_id: int = Field(index=True)
    details: str = ""
    created_at: datetime = Field(default_factory=utc_now)


class WorkSession(SQLModel, table=True):
    """Track actual time and task outcomes separately from cash payouts."""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_name: str = Field(index=True)
    minutes_spent: int
    reward_amount: str = "0"
    currency: str = Field(default="USD", index=True)
    status: str = Field(default="pending", index=True)
    started_at: datetime = Field(default_factory=utc_now, index=True)
    notes: str = ""
