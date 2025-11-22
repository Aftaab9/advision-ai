import numpy as np
import pandas as pd
import datetime as dt
import random
from pathlib import Path


def generate_campaign_data(n=1000, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    brand_names = [f"Brand_{i}" for i in range(1, 21)]
    categories = ["fashion", "beauty", "electronics", "luxury", "grocery"]
    platforms = ["instagram", "facebook", "youtube", "tiktok", "google_ads"]
    countries = ["IN", "SG", "US", "AE", "UK", "EU"]
    segments = [
        "Gen Z - Urban",
        "Millennial Professionals",
        "Families",
        "Students",
        "HNI / Affluent",
    ]

    rows = []
    start_base = dt.date(2023, 1, 1)

    for i in range(n):
        campaign_id = f"C{i+1:04d}"
        brand = random.choice(brand_names)
        cat = random.choice(categories)
        platform = random.choice(platforms)
        country = random.choice(countries)
        segment = random.choice(segments)

        # dates
        offset_days = random.randint(0, 730)  # ~2 years
        start_date = start_base + dt.timedelta(days=offset_days)
        duration = random.randint(7, 45)
        end_date = start_date + dt.timedelta(days=duration)

        # spend in USD
        platform_spend_factor = {
            "instagram": 1.0,
            "facebook": 0.9,
            "youtube": 1.3,
            "tiktok": 0.8,
            "google_ads": 1.5,
        }
        base_spend = np.random.gamma(shape=2.0, scale=300.0)  # mean ~600
        spend = base_spend * platform_spend_factor[platform]
        spend = float(np.clip(spend, 50, 20000))

        # impressions correlated with spend
        impressions_per_dollar = {
            "instagram": 150,
            "facebook": 180,
            "youtube": 80,
            "tiktok": 200,
            "google_ads": 120,
        }
        mean_impr = spend * impressions_per_dollar[platform]
        impressions = int(np.random.normal(loc=mean_impr, scale=0.25 * mean_impr))
        impressions = max(impressions, int(spend * 50))

        # reach a bit less than impressions
        reach = int(np.random.normal(loc=0.7 * impressions, scale=0.1 * impressions))
        reach = max(min(reach, impressions), int(0.3 * impressions))

        # CTR baseline per platform
        ctr_base = {
            "instagram": 0.012,
            "facebook": 0.01,
            "youtube": 0.008,
            "tiktok": 0.015,
            "google_ads": 0.02,
        }[platform]
        ctr = max(ctr_base + np.random.normal(0, 0.003), 0.001)
        clicks = int(impressions * ctr)

        # conversion rate per category
        conv_base = {
            "fashion": 0.03,
            "beauty": 0.035,
            "electronics": 0.02,
            "luxury": 0.015,
            "grocery": 0.04,
        }[cat]
        conv_rate = max(conv_base + np.random.normal(0, 0.01), 0.002)
        conversions = int(clicks * conv_rate)

        # average order value per category
        aov = {
            "fashion": 50,
            "beauty": 40,
            "electronics": 200,
            "luxury": 400,
            "grocery": 30,
        }[cat]
        revenue = conversions * aov

        currency = "USD"

        # synthetic ad text
        ad_text_templates = [
            "Limited time offer on our {cat} collection. Shop now and save big!",
            "Discover premium {cat} curated for {segment}. Click to explore.",
            "New arrivals in {cat} just dropped. Don't miss out!",
            "Upgrade your {cat} game with exclusive deals for {country}.",
            "Top-rated {cat} loved by customers like you. Check it out.",
        ]
        tmpl = random.choice(ad_text_templates)
        ad_text = tmpl.format(cat=cat, segment=segment, country=country)

        primary_cta = random.choice(["Shop now", "Learn more", "Sign up", "Get offer"])
        image_path = f"images/{campaign_id.lower()}.jpg"  # placeholder for now

        row = dict(
            campaign_id=campaign_id,
            brand_name=brand,
            product_category=cat,
            platform=platform,
            country=country,
            target_segment=segment,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            ad_text=ad_text,
            primary_call_to_action=primary_cta,
            image_path=image_path,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            reach=reach,
            spend=round(spend, 2),
            revenue=revenue,
            currency=currency,
        )
        rows.append(row)

    df = pd.DataFrame(rows)

    # derived metrics
    df["ctr"] = df["clicks"] / df["impressions"].replace(0, np.nan)
    df["conversion_rate"] = df["conversions"] / df["clicks"].replace(0, np.nan)
    df["engagement_rate"] = (df["clicks"] + df["conversions"]) / df["impressions"].replace(
        0, np.nan
    )
    df["roi"] = (df["revenue"] - df["spend"]) / df["spend"]

    # viral label: top 15% by engagement_rate
    threshold = df["engagement_rate"].quantile(0.85)
    df["is_viral"] = (df["engagement_rate"] >= threshold).astype(int)

    return df


if __name__ == "__main__":
    output_path = Path("data") / "campaigns_synthetic.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_campaign_data(n=1000, seed=42)
    df.to_csv(output_path, index=False)

    print(f"Saved synthetic dataset to {output_path.resolve()}")
