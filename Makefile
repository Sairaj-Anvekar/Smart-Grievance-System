# ============================================================
# Smart Grievance System — Makefile
# Common commands for development
# ============================================================

.PHONY: help up down logs backend frontend test lint clean

# Default target
help: ## Show this help
	@echo.
	@echo   Smart Grievance System - Commands
	@echo   =================================
	@echo.
	@echo   up          Start all services (Docker Compose)
	@echo   down        Stop all services
	@echo   logs        Tail all service logs
	@echo   backend     Run backend locally (no Docker)
	@echo   frontend    Run frontend locally (no Docker)
	@echo   test        Run backend tests
	@echo   lint        Lint backend code
	@echo   migrate     Run database migrations
	@echo   seed        Seed database with sample data
	@echo   clean       Remove all containers, volumes, caches
	@echo.

# ---------- Docker ----------
up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## Tail logs
	docker compose logs -f

rebuild: ## Rebuild and restart
	docker compose down
	docker compose build --no-cache
	docker compose up -d

# ---------- Backend ----------
backend: ## Run backend locally
	cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run backend tests
	cd backend && python -m pytest tests/ -v

lint: ## Lint backend
	cd backend && python -m ruff check .

format: ## Format backend code
	cd backend && python -m ruff format .

# ---------- Frontend ----------
frontend: ## Run frontend dev server
	cd frontend && npm run dev

frontend-build: ## Build frontend for production
	cd frontend && npm run build

# ---------- Database ----------
migrate: ## Run Alembic migrations
	cd backend && alembic upgrade head

migrate-new: ## Create new migration
	cd backend && alembic revision --autogenerate -m "$(msg)"

seed: ## Seed database with sample data
	cd backend && python -m app.utils.seed

# ---------- Cleanup ----------
clean: ## Remove containers, volumes, caches
	docker compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
