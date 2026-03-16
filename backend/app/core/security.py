"""JWT 创建/验证/吊销 + 密码哈希"""

import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.cache.client import get_redis_client
from app.cache.keys import CacheKeys
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """对密码进行 bcrypt 哈希"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """验证明文密码与哈希是否匹配"""
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, role: str = "admin") -> tuple[str, str]:
    """
    创建 access token。

    Returns:
        (token, jti) 元组，jti 用于 Redis 黑名单
    """
    jti = str(uuid.uuid4())
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": jti,
        "exp": expire,
        "type": "access",
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, jti


def create_refresh_token(user_id: int) -> str:
    """创建 refresh token（存于 httpOnly Cookie）"""
    expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    """
    解码并验证 JWT。

    Raises:
        JWTError: token 无效或已过期
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


async def revoke_token(jti: str, expire_seconds: int) -> None:
    """将 token jti 加入 Redis 黑名单"""
    redis = await get_redis_client()
    await redis.setex(CacheKeys.jwt_blacklist(jti), expire_seconds, "1")


async def is_token_revoked(jti: str) -> bool:
    """检查 token 是否已被吊销"""
    redis = await get_redis_client()
    return await redis.exists(CacheKeys.jwt_blacklist(jti)) == 1
