# ARK_MEMORY_SYSTEM_ACTIVE
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "The Pharos"
    API_V1_STR: str = "/api/v1"
    # LLM model used by the AI Scoring Engine.
    # Override via REVIEW_MODEL env var (e.g. "openai/gpt-4o").
    REVIEW_MODEL: str = "gemini/gemini-2.5-flash"

    class Config:
        env_file = ".env"


settings = Settings()