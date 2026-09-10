# Sairaj — Backend + DevOps + Cloud

> **Role:** Backend Developer, DevOps Engineer, Cloud Architect
> **Primary Workspace:** `backend/`, `infra/`, `.github/`, root configs

---

## 🎯 What You Own

| Area               | Directories / Files                                      |
|--------------------|----------------------------------------------------------|
| **Backend API**    | `backend/app/api/`, `backend/app/services/`              |
| **Database**       | `backend/app/models/`, `backend/app/schemas/`, `backend/alembic/` |
| **Background Jobs**| `backend/app/tasks/`                                     |
| **Config & Auth**  | `backend/app/config.py`, `backend/app/utils/`            |
| **Infrastructure** | `infra/docker-compose.yml`, `infra/nginx/`, `infra/scripts/` |
| **CI/CD**          | `.github/workflows/`                                     |
| **Cloud (AWS)**    | EC2 setup, S3 bucket config, SSM, deploy scripts         |

---

## 📋 Key Responsibilities

### Phase 1 — Foundation (Weeks 1–2)
- [ ] Set up project scaffolding (FastAPI, Docker Compose, PostgreSQL + PostGIS, Redis, MinIO)
- [ ] Implement database models: `Complaint`, `User`, `Worker`, `Assignment`
- [ ] Create Alembic migrations
- [ ] Build core CRUD API endpoints (`/complaints`, `/users`)
- [ ] Set up authentication (JWT-based, role-based access)

### Phase 2 — Core Features (Weeks 3–4)
- [ ] Implement complaint lifecycle (submit → classify → assign → resolve → close)
- [ ] Build worker assignment & task queue logic
- [ ] Integrate Celery + Redis for background tasks (SLA checks, notifications)
- [ ] File upload endpoint (photos → MinIO/S3)
- [ ] Integrate ML model serving endpoints (coordinate with Tushar)

### Phase 3 — Integrations (Weeks 5–6)
- [ ] Telegram Bot webhook integration (`python-telegram-bot`)
- [ ] Notification service (email / Telegram alerts)
- [ ] Geospatial queries with PostGIS (nearby complaints, hotspot detection)
- [ ] API rate limiting & security hardening
- [ ] Write API tests (`backend/tests/`)

### Phase 4 — DevOps & Deployment (Weeks 7–8)
- [ ] Finalize Docker Compose for production
- [ ] Set up Nginx reverse proxy config
- [ ] GitHub Actions CI pipeline (lint, test, build)
- [ ] Deploy to AWS EC2 (free tier)
- [ ] Configure S3, SSM, and domain/SSL

---

## 🔗 Coordination Points

| With      | What                                                                 |
|-----------|----------------------------------------------------------------------|
| **Sufiyan** | Define and document API contracts (request/response schemas) so frontend can develop in parallel |
| **Tushar**  | Provide model-serving endpoints (`POST /api/classify/image`, `POST /api/classify/text`), agree on input/output formats |

---

## 📚 Learning Resources

- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [GitHub Actions Quickstart](https://docs.github.com/en/actions/quickstart)

---

## 📝 Personal Notes

> Use this space for your own notes, blockers, questions, or ideas.
> This file is gitignored — it's your private scratchpad.

- 

