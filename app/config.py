# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Crop Disease Detection System"
    DESCRIPTION: str = "Premium SaaS Agricultural Diagnostics Engine"
    APP_VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    WORKERS: int = 1

    class Config:
        env_file = ".env"

settings = Settings()