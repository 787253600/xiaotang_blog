"""认证业务逻辑：登录/注销/刷新 token"""

from datetime import UTC, datetime

from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    revoke_token,
    verify_password,
)
from app.domains.auth.models import User
from app.domains.auth.schemas import LoginRequest, TokenResponse, UserInfo


class AuthService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def login(self, data: LoginRequest) -> tuple[TokenResponse, str]:
        """
        登录验证，返回 (access_token_response, refresh_token)。
        refresh_token 由调用方写入 httpOnly Cookie。
        """
        user = await self._get_user_by_username(data.username)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("用户名或密码错误")

        if not user.is_active:
            raise UnauthorizedError("账号已被禁用")

        access_token, _ = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return TokenResponse(access_token=access_token), refresh_token

    async def logout(self, access_token: str) -> None:
        """注销：将 access token 加入 Redis 黑名单"""
        try:
            payload = decode_token(access_token)
            jti = payload.get("jti")
            exp = payload.get("exp", 0)
            if jti:
                remaining = max(0, exp - int(datetime.now(UTC).timestamp()))
                await revoke_token(jti, remaining)
        except JWTError:
            pass  # token 已过期，无需处理

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """使用 refresh token 换取新的 access token"""
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise UnauthorizedError("token 类型错误")
            user_id = int(payload["sub"])
        except (JWTError, KeyError, ValueError):
            raise UnauthorizedError("refresh token 无效")

        user = await self._session.get(User, user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("用户不存在或已禁用")

        access_token, _ = create_access_token(user_id)
        return TokenResponse(access_token=access_token)

    async def get_current_user(self, user_id: int) -> UserInfo:
        user = await self._session.get(User, user_id)
        if not user:
            raise UnauthorizedError("用户不存在")
        return UserInfo.model_validate(user)

    async def change_password(
        self, user_id: int, current_password: str, new_password: str
    ) -> None:
        """修改当前用户密码"""
        from app.core.exceptions import BadRequestError
        user = await self._session.get(User, user_id)
        if not user:
            raise UnauthorizedError("用户不存在")
        if not verify_password(current_password, user.hashed_password):
            raise BadRequestError("当前密码错误")
        user.hashed_password = hash_password(new_password)
        await self._session.commit()

    async def _get_user_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
