# ML Pipeline Design – AdVision AI

## 1. Objective
Predict marketing outcomes such as:
- Engagement Rate
- ROI
- Virality (binary classification)

## 2. Inputs
- Campaign metadata (platform, country, category)
- Spend & reach metrics
- Text (ad copy) [future]
- Image features (creative) [future]

## 3. Current Baseline Model
- RandomForestRegressor → Engagement Rate prediction
- OneHotEncoder for categorical variables
- Trained on synthetic dataset

## 4. Next Enhancements
1. Add NLP embeddings (ad_text using BERT)
2. Add image embeddings (ResNet/EfficientNet)
3. Build a multi-input deep learning model
4. Add hyperparameter optimization
5. Convert to FastAPI service
