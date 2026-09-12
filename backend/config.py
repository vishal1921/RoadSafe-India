from pydantic_settings import BaseSettings
from typing import List


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_FILE = (BASE_DIR / "road_safety.db").as_posix()


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    APP_NAME: str = "Road Safety AI System"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{DEFAULT_DB_FILE}"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
