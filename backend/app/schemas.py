
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
    model_version_str: str = "baseline_v1"


# --- New schemas below --- #

class CampaignBase(BaseModel):
    platform: str
    country: str
    product_category: str
    spend: float
    impressions: int
    clicks: int
    conversions: int
    reach: int


class CampaignCreate(CampaignBase):
    pass


class CampaignOut(CampaignBase):
    id: int
    predicted_engagement_rate: float

    class Config:
        from_attributes = True  # SQLAlchemy -> Pydantic
