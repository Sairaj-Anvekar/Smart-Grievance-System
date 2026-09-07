"""
Smart Grievance System — Application Configuration

Loads settings from environment variables / .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- App ---
    APP_NAME: str = "smart-grievance-system"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # --- Backend ---
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    JWT_SECRET: str = "change-me-to-a-random-64-char-string"
    JWT_ALGORITHM: str = "HS256"
    ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ADMIN_REFRESH_TOKEN_EXPIRE_HOURS: int = 24
    WORKER_ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://grievance_user:change-me@localhost:5432/grievance_db"

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # --- Storage ---
    STORAGE_BACKEND: str = "minio"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "grievance-uploads"
    MINIO_USE_SSL: bool = False

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_SECRET: str = ""
    TELEGRAM_WEBHOOK_URL: str = ""

    # --- Session ---
    SESSION_TTL_MINUTES: int = 30
    SESSION_IDLE_PROMPT_MINUTES: int = 15

    # --- Task Allocation ---
    WORKER_DAILY_TASK_LIMIT: int = 20
    SHIFT_START_HOUR: int = 6
    PRIORITY_WEIGHT: float = 0.40
    ELAPSED_TIME_WEIGHT: float = 0.35
    QUEUE_POSITION_WEIGHT: float = 0.15
    CARRY_FORWARD_WEIGHT: float = 0.10

    # --- Rate Limiting ---
    ADMIN_LOGIN_RATE_LIMIT: str = "3/minute"
    WORKER_LOGIN_RATE_LIMIT: str = "5/hour"
    CITIZEN_COMPLAINT_RATE_LIMIT: str = "5/day"

    # --- AI/ML ---
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.70
    AUTO_REJECT_CONFIDENCE_THRESHOLD: float = 0.50

    # --- CORS ---
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
