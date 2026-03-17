"""全局配置管理 - 基于 Pydantic Settings，支持 .env 文件与环境变量"""

import warnings
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 应用
    app_name: str = "小汤博客"
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

    # CORS（逗号分隔字符串，validator 负责转换为 list）
    allowed_origins: str = "http://localhost:3000"

    # 管理员初始账户
    admin_username: str = "admin"
    admin_password: str = "changeme123"
    admin_email: str = "admin@example.com"

    # 分页
    default_page_size: int = 10
    max_page_size: int = 100

    @property
    def allowed_origins_list(self) -> list[str]:
        """将逗号分隔的 CORS 字符串转换为列表"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @model_validator(mode="after")
    def check_secret_key(self) -> "Settings":
        """生产环境下，若使用默认 SECRET_KEY 则发出警告"""
        default_keys = {"your-secret-key-change-in-production", "changeme", "secret"}
        if not self.debug and self.secret_key in default_keys:
            warnings.warn(
                "SECRET_KEY 使用了不安全的默认值，生产环境请在 .env 中设置强随机密钥！",
                stacklevel=2,
            )
        return self


@lru_cache
def get_settings() -> Settings:
    """单例配置，应用启动后全局复用"""
    return Settings()
