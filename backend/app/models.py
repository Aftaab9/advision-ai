from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    country = Column(String, index=True)
    product_category = Column(String, index=True)

    spend = Column(Float)
    impressions = Column(Integer)
    clicks = Column(Integer)
    conversions = Column(Integer)
    reach = Column(Integer)

    predicted_engagement_rate = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
