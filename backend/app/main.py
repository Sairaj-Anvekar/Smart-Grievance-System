"""
Smart Grievance System — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="Smart Grievance System",
    description="AI-powered civic grievance platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "smart-grievance-system"}


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check — verifies DB and Redis connectivity."""
    # TODO: Add actual DB and Redis ping checks
    return {"status": "ready"}


# --- Register API Routers ---
# TODO: Include routers as they are built
# from app.api.v1 import auth, complaints, workers, admin, telegram, health
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaints"])
# app.include_router(workers.router, prefix="/api/v1/workers", tags=["Workers"])
# app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
# app.include_router(telegram.router, prefix="/api/v1/webhook", tags=["Telegram"])
