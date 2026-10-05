import os
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    APP_NAME: str = "Hospital Management System API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql://postgres:postgres@127.0.0.1:5432/hospital_management_system"

    SECRET_KEY: str = "hms_jwt_secret_key_change_in_production_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    SEED_ADMIN_USERNAME: str = "admin"
    SEED_ADMIN_PASSWORD: str = "admin123"
    SEED_ADMIN_EMAIL: str = "admin@hms.com"

    AI_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:4b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    RAG_TOP_K: int = 3

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Production Security Check
if settings.ENVIRONMENT.lower() == "production":
    if settings.SECRET_KEY == "hms_jwt_secret_key_change_in_production_2026":
        raise ValueError("CRITICAL SECURITY ERROR: Default SECRET_KEY cannot be used in production environment!")
    if "postgres:postgres@" in settings.DATABASE_URL or "KANISHAJAI" in settings.DATABASE_URL:
        raise ValueError("CRITICAL SECURITY ERROR: Default/Insecure DATABASE_URL credentials cannot be used in production environment!")


