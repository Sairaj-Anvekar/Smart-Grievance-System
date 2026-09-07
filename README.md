# Smart Grievance System

> **A Smart Civic Grievance Platform** — AI-powered complaint management connecting citizens, field workers, and administrators through one intelligent system.

[![CI](https://github.com/SairajA07/smart-grievance-system/actions/workflows/ci.yml/badge.svg)](https://github.com/SairajA07/smart-grievance-system/actions/workflows/ci.yml)

---

## What It Does

| User | Interface | Experience |
|------|-----------|------------|
| 🧑‍🤝‍🧑 **Citizen** | Telegram Bot | Report a civic issue in 30 seconds — snap a photo, share location, done |
| 👷 **Field Worker** | Mobile PWA | See daily task queue with priority scoring, navigate to locations, submit resolution proof |
| 🏛️ **Administrator** | Web Dashboard | Real-time analytics, hotspot maps, triage queue, worker performance |

## Architecture

```
Telegram Bot ──┐
               ├──► FastAPI Backend ──► PostgreSQL + PostGIS
Web Dashboard ─┤        │                    │
Mobile PWA ────┘   AI/ML Engine         Redis (Cache + Queue)
                   (MobileNetV2 +            │
                    DistilBERT)          MinIO/S3 (Photos)
```

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, Celery, Redis |
| **Frontend** | Vue 3 (Composition API), Bootstrap 5, Vite, Pinia, Chart.js, Leaflet |
| **AI/ML** | MobileNetV2 (image), DistilBERT (text), TensorFlow/Keras |
| **Database** | PostgreSQL 16 + PostGIS |
| **Infrastructure** | Docker, Docker Compose, GitHub Actions, Nginx |
| **Cloud** | AWS EC2 (Free Tier), S3, SSM |

## Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/downloads)

### Run Locally

```bash
# Clone the repo
git clone https://github.com/SairajA07/smart-grievance-system.git
cd smart-grievance-system

# Copy environment variables
cp .env.example .env

# Start everything
docker compose up -d

# Backend API:    http://localhost:8000
# API Docs:       http://localhost:8000/docs
# Frontend:       http://localhost:5173
# MinIO Console:  http://localhost:9001
```

### Development (without Docker)

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Project Structure

```
smart-grievance-system/
├── backend/              # FastAPI + Celery backend
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── ml/           # AI/ML classifiers
│   │   ├── tasks/        # Celery background tasks
│   │   └── utils/        # Helpers
│   └── tests/
├── frontend/             # Vue 3 + Bootstrap 5 PWA
│   └── src/
├── ml-training/          # Jupyter notebooks (Colab)
├── infra/                # Docker Compose, Nginx, deploy scripts
└── docs/                 # Architecture & API docs
```

## Team

| Role | Member |
|------|--------|
| Backend + DevOps + Cloud | **Sairaj** |
| Frontend | **Sufiyan** |
| ML / AI | **Tushar** |

## License

This project is part of a college semester project and is not licensed for commercial use.
