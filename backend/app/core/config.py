from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    THECATAPI_BASE: str = "https://api.thecatapi.com/v1/breeds"
    THECATAPI_KEY: str | None = None
    CORS_ORIGINS: str = "http://localhost:3000"
    class Config:
        env_file = ".env"

settings = Settings()
