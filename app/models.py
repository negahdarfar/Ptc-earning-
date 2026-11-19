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
