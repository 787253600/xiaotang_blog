"""认证路由 /api/v1/auth"""

from fastapi import APIRouter, Cookie, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies import CurrentUserID, DBSession
from app.domains.auth.schemas import ChangePasswordRequest, LoginRequest, TokenResponse, UserInfo
from app.domains.auth.service import AuthService
from app.schemas.response import Response as AppResponse

router = APIRouter(prefix="/auth", tags=["认证"])
_bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=AppResponse[TokenResponse])
async def login(
    body: LoginRequest,
    response: Response,
    session: DBSession,
):
    service = AuthService(session)
    token_resp, refresh_token = await service.login(body)

    # refresh_token 存入 httpOnly Cookie，防止 XSS 读取
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,   # 生产环境改为 True（HTTPS）
        samesite="lax",
        max_age=7 * 24 * 3600,
    )
    return AppResponse(data=token_resp)


@router.post("/logout", response_model=AppResponse[None])
async def logout(
    response: Response,
    session: DBSession,
    user_id: CurrentUserID,
    credentials: HTTPAuthorizationCredentials = None,
):
    service = AuthService(session)
    if credentials:
        await service.logout(credentials.credentials)
    response.delete_cookie("refresh_token")
    return AppResponse(message="已退出登录")


@router.post("/refresh", response_model=AppResponse[TokenResponse])
async def refresh_token(
    session: DBSession,
    refresh_token: str | None = Cookie(default=None),
):
    if not refresh_token:
        from app.core.exceptions import UnauthorizedError
        raise UnauthorizedError("缺少 refresh_token")
    service = AuthService(session)
    data = await service.refresh(refresh_token)
    return AppResponse(data=data)


@router.get("/me", response_model=AppResponse[UserInfo])
async def get_me(session: DBSession, user_id: CurrentUserID):
    service = AuthService(session)
    data = await service.get_current_user(user_id)
    return AppResponse(data=data)


@router.patch("/password", response_model=AppResponse[None])
async def change_password(
    body: ChangePasswordRequest,
    session: DBSession,
    user_id: CurrentUserID,
):
    service = AuthService(session)
    await service.change_password(user_id, body.current_password, body.new_password)
    return AppResponse(message="密码已修改")
