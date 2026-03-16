"""全局配置管理 - 基于 Pydantic Settings，支持 .env 文件与环境变量"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 应用
    app_name: str = "小唐博客"
    app_version: str = "0.1.0"
    debug: bool = False

    # 数据库
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000"]

    # 管理员初始账户
    admin_username: str = "admin"
    admin_password: str = "changeme123"
    admin_email: str = "admin@example.com"

    # 分页
    default_page_size: int = 10
    max_page_size: int = 100

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """单例配置，应用启动后全局复用"""
    return Settings()
