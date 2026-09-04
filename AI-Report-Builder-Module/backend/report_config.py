import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REPORT_BUILDER_ENABLED: bool = True
    REPORT_DATA_SOURCE: str = "csv"
    REPORT_STORAGE_PATH: str = "./reports/storage"
    OLLAMA_ENABLED: bool = True
    OLLAMA_MODEL: str = "qwen3:4b"
    OLLAMA_HOST: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()

if settings.REPORT_BUILDER_ENABLED and not os.path.exists(settings.REPORT_STORAGE_PATH):
    os.makedirs(settings.REPORT_STORAGE_PATH)
