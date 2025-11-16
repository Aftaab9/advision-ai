# AdVision AI – Marketing & ROI Intelligence Platform

AdVision AI is an end-to-end, cloud-ready platform that helps marketers and decision-makers:
- Analyze past digital marketing campaigns
- Predict virality, engagement, and ROI using deep learning and NLP
- Simulate “what-if” scenarios for budget allocation across channels

## Tech Stack

- **Frontend:** React / Next.js
- **Backend:** FastAPI (Python)
- **ML:** PyTorch, HuggingFace Transformers, transfer learning (vision + NLP)
- **Database:** PostgreSQL
- **Cloud:** AWS (EC2, S3), Docker, docker-compose
- **Other:** GitHub for version control, Cursor for development

## High-Level Architecture

- `frontend/` – User-facing dashboard and campaign upload UI
- `backend/` – REST API for data, predictions, and simulation
- `notebooks/` – Jupyter notebooks for data exploration and model training
- `db/` – SQL schema, ER diagrams, and migrations
- `docs/` – Project documentation and design notes
- `infra/` – Docker and deployment configuration

## Roadmap (Phase 1)

1. Generate a synthetic marketing campaign dataset
2. Train initial ML models to predict engagement and ROI (tabular)
3. Build basic FastAPI backend exposing prediction APIs
4. Create a minimal frontend to upload data and view predictions
5. Containerize services using Docker and docker-compose

More features (NLP on ad copy, image-based creative analysis, advanced finance metrics) will be added iteratively.
