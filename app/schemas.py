from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

class OpportunityCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=60)
    platform_url: HttpUrl
    country_eligibility: str = "unknown"
    payout_method: str = "unknown"
    payout_currency: str = "USD"
    minimum_payout: str = "unknown"
    estimated_rate: str = "unknown"
    official_api: bool = False
    terms_verified: bool = False
    status: str = "pending"
    notes: str = ""

class OpportunityRead(OpportunityCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class RevenueCreate(BaseModel):
    source_name: str = Field(min_length=2, max_length=120)
    amount: str = Field(pattern=r"^\d+(\.\d{1,8})?$")
    currency: str = Field(default="USD", min_length=2, max_length=10)
    status: str = "pending"
    payout_reference: str = ""
    notes: str = ""

class RevenueRead(RevenueCreate):
    id: int
    recorded_at: datetime
    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    source_name: str = Field(min_length=2, max_length=120)
    amount: str = Field(pattern=r"^\d+(\.\d{1,8})?$")
    currency: str = Field(default="USD", min_length=2, max_length=10)
    status: str = "paid"
    notes: str = ""

class ExpenseRead(ExpenseCreate):
    id: int
    recorded_at: datetime
    class Config:
        from_attributes = True

class DigitalProductCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    category: str = Field(min_length=2, max_length=60)
    language: str = Field(default="en", min_length=2, max_length=12)
    short_description: str = Field(min_length=10, max_length=500)
    full_description: str = Field(default="", max_length=10000)
    price_amount: str = Field(default="0", pattern=r"^\d+(\.\d{1,8})?$")
    price_currency: str = Field(default="USD", min_length=2, max_length=10)
    asset_url: HttpUrl | None = None
    rights_confirmed: bool = False
    status: str = "draft"

class DigitalProductRead(DigitalProductCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class OpportunityEvidenceCreate(BaseModel):
    evidence_url: HttpUrl
    reviewed_on: datetime
    country_eligibility: str = Field(default="unknown", min_length=2, max_length=120)
    kyc_summary: str = Field(default="unknown", max_length=500)
    payout_method: str = Field(default="unknown", max_length=80)
    payout_currency: str = Field(default="USD", min_length=2, max_length=10)
    minimum_payout: str = Field(default="unknown", max_length=40)
    payout_fee_percent: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    average_reward: str = Field(default="0", pattern=r"^\d+(\.\d{1,8})?$")
    estimated_task_minutes: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    approval_rate_percent: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    reviewer_notes: str = Field(default="", max_length=2000)


class OpportunityEvidenceRead(OpportunityEvidenceCreate):
    id: int
    opportunity_id: int
    created_at: datetime
    class Config:
        from_attributes = True


class WorkSessionCreate(BaseModel):
    source_name: str = Field(min_length=2, max_length=120)
    minutes_spent: int = Field(ge=1, le=1440)
    reward_amount: str = Field(default="0", pattern=r"^\d+(\.\d{1,8})?$")
    currency: str = Field(default="USD", min_length=3, max_length=10)
    status: str = Field(default="pending", pattern=r"^(pending|approved|rejected|abandoned)$")
    started_at: datetime | None = None
    notes: str = Field(default="", max_length=2000)


class WorkSessionRead(WorkSessionCreate):
    id: int
    started_at: datetime
    class Config:
        from_attributes = True


class SourceLeadCreate(BaseModel):
    platform_key: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9][a-z0-9-]*$")
    platform_name: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=60)
    source_url: HttpUrl
    source_type: str = Field(default="manual_only", pattern=r"^(manual_only|official_api|affiliate|digital_product|client_services|microtask|research)$")
    review_notes: str = Field(default="", max_length=2000)


class SourceLeadRead(SourceLeadCreate):
    id: int
    official_terms_url: str
    review_status: str
    country_eligibility: str
    payout_method: str
    payout_currency: str
    minimum_payout: str
    official_api: bool
    reviewed_on: str | None
    payout_fee_percent: str
    average_reward: str
    estimated_task_minutes: str
    approval_rate_percent: str
    opportunity_id: int | None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class SourceLeadReview(BaseModel):
    review_status: str = Field(pattern=r"^(researching|needs_operator|rejected|approved)$")
    official_terms_url: HttpUrl | None = None
    reviewed_on: datetime | None = None
    country_eligibility: str = Field(default="unknown", min_length=2, max_length=120)
    payout_method: str = Field(default="unknown", max_length=80)
    payout_currency: str = Field(default="unknown", min_length=2, max_length=10)
    minimum_payout: str = Field(default="unknown", max_length=40)
    official_api: bool = False
    payout_fee_percent: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    average_reward: str = Field(default="0", pattern=r"^\d+(\.\d{1,8})?$")
    estimated_task_minutes: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    approval_rate_percent: str = Field(default="0", pattern=r"^\d+(\.\d{1,4})?$")
    review_notes: str = Field(default="", max_length=2000)


class SourceLeadDecisionRead(BaseModel):
    lead: SourceLeadRead
    opportunity: OpportunityRead | None = None
