from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "PICK-E House Manager"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    DATABASE_URL: str = "sqlite:///./picke.db"
    
    # REDIS
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # SECURITY
    SECRET_KEY: str = "CHANGEME_SUPER_SECRET_KEY"  # In production, use a strong secret
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AGENTS
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    GOOGLE_CLOUD_REGION: str = "us-central1"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # EXTERNAL INTEGRATIONS
    TRELLO_API_KEY: Optional[str] = None
    TRELLO_TOKEN: Optional[str] = None
    NOTION_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
