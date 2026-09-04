import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PREDICTIVE_ANALYTICS_ENABLED: bool = True
    DATA_SOURCE: str = "mock"
    DATABASE_URL: str = ""
    FORECAST_HORIZON: int = 30
    MODEL_TYPE: str = "LinearRegression"
    OLLAMA_ENABLED: bool = True
    OLLAMA_MODEL: str = "qwen3:4b" # or any available model like llama3
    OLLAMA_HOST: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()
