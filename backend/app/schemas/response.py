"""统一响应格式"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """单对象响应"""
    code: int = 0
    message: str = "success"
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页列表响应"""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
