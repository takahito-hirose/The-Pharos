from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Create a .env file in the root directory to set these values.
    Example:
    LLM_API_KEY="your_openai_api_key"
    LLM_MODEL="gpt-4o"
    """
    LLM_API_KEY: str = "your_llm_api_key_here"
    LLM_MODEL: str = "gpt-4o"
    GITHUB_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()