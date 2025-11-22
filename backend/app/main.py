from fastapi import FastAPI
from .schemas import EngagementRequest, EngagementResponse
import joblib
import pathlib
import pandas as pd   # ⬅ add this



app = FastAPI(
    title="AdVision AI Backend",
    description="API for marketing engagement predictions",
    version="0.1.0",
)

# Load model at startup
MODEL_PATH = pathlib.Path(__file__).resolve().parent.parent / "model_engagement_rate.pkl"
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok", "message": "AdVision AI backend is running"}

@app.post("/predict-engagement", response_model=EngagementResponse)
def predict_engagement(payload: EngagementRequest):
    """
    Predict engagement rate using baseline RandomForest model.
    """

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

    # Create a single-row DataFrame with the same columns as during training
    X = pd.DataFrame([data])

    pred = model.predict(X)[0]

    return EngagementResponse(
        engagement_rate=float(pred),
        model_version="baseline_v1",
    )


# @app.post("/predict-engagement", response_model=EngagementResponse)
# def predict_engagement(payload: EngagementRequest):
#     """
#     Predict engagement rate using baseline RandomForest model.
#     """

#     # Build input in the same order as training features
#     X = [{
#         "platform": payload.platform,
#         "country": payload.country,
#         "product_category": payload.product_category,
#         "spend": payload.spend,
#         "impressions": payload.impressions,
#         "clicks": payload.clicks,
#         "conversions": payload.conversions,
#         "reach": payload.reach,
#     }]

#     pred = model.predict(X)[0]

#     return EngagementResponse(
#         engagement_rate=float(pred),
#         model_version="baseline_v1",
#     )
