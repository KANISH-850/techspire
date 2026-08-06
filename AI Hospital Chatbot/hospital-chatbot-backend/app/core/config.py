from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "AI Hospital Chatbot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "hospital_chatbot"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"

    @property
    def DATABASE_URL(self) -> str:
        return "sqlite:///./hospital_chatbot.db"
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Provider settings
    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Model configuration
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """
    Cached function to return application settings.
    This ensures that .env is read only once.
    """
    return Settings()


settings = get_settings()
