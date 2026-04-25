# ARK_MEMORY_SYSTEM_ACTIVE
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    REVIEW_MODEL: str = "gemini/gemini-2.5-flash"
    
    # 修正ポイント1: APIキーを明示的に受け入れるように定義
    gemini_api_key: Optional[str] = None

    # 修正ポイント2: 他の知らない環境変数が来てもエラーにせず「無視」する設定
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()