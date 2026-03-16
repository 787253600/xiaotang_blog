"""自定义异常类与全局异常处理器"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, code: int, message: str, detail: str = "", status_code: int = 400):
        self.code = code
        self.message = message
        self.detail = detail
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, resource: str = "资源"):
        super().__init__(
            code=4004,
            message=f"{resource}不存在",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "请先登录"):
        super().__init__(
            code=4001,
            message="未授权",
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenError(AppException):
    def __init__(self, detail: str = "权限不足"):
        super().__init__(
            code=4003,
            message="禁止访问",
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ConflictError(AppException):
    def __init__(self, message: str = "资源已存在"):
        super().__init__(
            code=4009,
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


class ValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(
            code=4022,
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 5000,
                "message": "服务器内部错误",
                "detail": str(exc) if app.debug else "",
            },
        )
