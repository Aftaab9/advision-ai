
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends


from fastapi import FastAPI, Depends
from .schemas import (
    EngagementRequest,
    EngagementResponse,
    CampaignCreate,
    CampaignOut,
)
import joblib
import pathlib
import pandas as pd

from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models

from .models import Campaign
# Create tables (only runs if they don't exist)
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="AdVision AI Backend",
    description="API for marketing engagement predictions",
    version="0.1.0",
)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "model_engagement_rate.pkl"
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok", "message": "AdVision AI backend is running"}

@app.post("/predict-engagement", response_model=EngagementResponse)
def predict_engagement(payload: EngagementRequest):
    data = {
        "platform": payload.platform,
        "country": payload.country,
        "product_category": payload.product_category,
        "spend": payload.spend,
        "impressions": payload.impressions,
        "clicks": payload.clicks,
        "conversions": payload.conversions,
        "reach": payload.reach,
    }

    x_df = pd.DataFrame([data])
    pred = model.predict(x_df)[0]



    return EngagementResponse(
    engagement_rate=float(pred),
    model_version_str="baseline_v1",
)



@app.post(
    "/campaigns/create-with-prediction",
    response_model=CampaignOut,
    summary="Create a campaign, predict engagement, and store in DB",
)
def create_campaign_with_prediction(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
):
    # Build data for the ML model
    data = {
        "platform": payload.platform,
        "country": payload.country,
        "product_category": payload.product_category,
        "spend": payload.spend,
        "impressions": payload.impressions,
        "clicks": payload.clicks,
        "conversions": payload.conversions,
        "reach": payload.reach,
    }

    x_df = pd.DataFrame([data])
    pred = model.predict(x_df)[0]

    pred_float = float(pred)

    # Create ORM object
    campaign = models.Campaign(
        platform=payload.platform,
        country=payload.country,
        product_category=payload.product_category,
        spend=payload.spend,
        impressions=payload.impressions,
        clicks=payload.clicks,
        conversions=payload.conversions,
        reach=payload.reach,
        predicted_engagement_rate=pred_float,
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    return CampaignOut(
        id=campaign.id,
        platform=campaign.platform,
        country=campaign.country,
        product_category=campaign.product_category,
        spend=campaign.spend,
        impressions=campaign.impressions,
        clicks=campaign.clicks,
        conversions=campaign.conversions,
        reach=campaign.reach,
        predicted_engagement_rate=campaign.predicted_engagement_rate,
    )

@app.get("/campaigns", response_model=List[CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = (
        db.query(models.Campaign)
        .order_by(models.Campaign.created_at.desc())
        .limit(100)
        .all()
    )
    return campaigns



# ... keep your existing code above (models, get_db, etc.) ...

@app.get("/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).all()

    if not campaigns:
        return {
            "total_campaigns": 0,
            "total_spend": 0.0,
            "avg_ctr": 0.0,
            "platform_engagement": {},
        }

    total_spend = 0.0
    total_impressions = 0
    total_clicks = 0

    platform_engagement = {}

    for c in campaigns:
        # Be defensive: treat None as 0
        spend = float(c.spend or 0)
        impr = int(c.impressions or 0)
        clicks = int(c.clicks or 0)
        er = float(c.predicted_engagement_rate or 0.0)

        total_spend += spend
        total_impressions += impr
        total_clicks += clicks

        plat = c.platform or "unknown"
        platform_engagement.setdefault(plat, []).append(er)

    avg_ctr = (total_clicks / total_impressions) if total_impressions else 0.0

    # Average engagement per platform
    for plat, vals in platform_engagement.items():
        if vals:
            platform_engagement[plat] = sum(vals) / len(vals)
        else:
            platform_engagement[plat] = 0.0

    return {
        "total_campaigns": len(campaigns),
        "total_spend": float(total_spend),
        "avg_ctr": float(avg_ctr),
        "platform_engagement": platform_engagement,
    }
