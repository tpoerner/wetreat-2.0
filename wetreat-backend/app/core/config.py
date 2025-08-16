from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "WeTreat Backend"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./wetreat.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    ADMIN_SIGNUP_TOKEN: str = os.getenv("ADMIN_SIGNUP_TOKEN", "")

settings = Settings()
