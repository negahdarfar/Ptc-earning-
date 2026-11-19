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
