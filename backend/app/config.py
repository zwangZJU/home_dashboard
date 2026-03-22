"""全局配置，从环境变量读取"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 数据库
    database_url: str = "sqlite+aiosqlite:///./devtrack.db"

    # JWT
    jwt_secret_key: str = "devtrack-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 小时

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_prefix": "DEVTRACK_", "env_file": ".env"}


settings = Settings()
