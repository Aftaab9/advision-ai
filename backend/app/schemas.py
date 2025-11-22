from pydantic import BaseModel


class EngagementRequest(BaseModel):
    platform: str
    country: str
    product_category: str
    spend: float
    impressions: int
    clicks: int
    conversions: int
    reach: int


class EngagementResponse(BaseModel):
    engagement_rate: float
    model_version: str = "baseline_v1"
