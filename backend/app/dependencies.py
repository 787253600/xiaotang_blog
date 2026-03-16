"""全局依赖注入函数"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.client import get_redis_client
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_token, is_token_revoked
from app.db.session import get_db

# 数据库会话依赖
DBSession = Annotated[AsyncSession, Depends(get_db)]

# Redis 客户端依赖
RedisClient = Annotated[Redis, Depends(get_redis_client)]

# Bearer Token 提取器
_bearer = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> int:
    """
    验证 Bearer Token，返回当前用户 ID。

    Raises:
        UnauthorizedError: token 缺失、无效或已吊销
    """
    if credentials is None:
        raise UnauthorizedError("缺少 Authorization Header")

    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise UnauthorizedError("token 无效或已过期")

    if payload.get("type") != "access":
        raise UnauthorizedError("token 类型错误")

    jti = payload.get("jti")
    if jti and await is_token_revoked(jti):
        raise UnauthorizedError("token 已被吊销，请重新登录")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("token 缺少用户信息")

    return int(user_id)


# 认证用户 ID 依赖
CurrentUserID = Annotated[int, Depends(get_current_user_id)]
