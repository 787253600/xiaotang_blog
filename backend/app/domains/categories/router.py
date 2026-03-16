"""分类路由 /api/v1/categories"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import CurrentUserID, DBSession
from app.domains.categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.domains.categories.service import CategoryService
from app.schemas.response import Response

router = APIRouter(prefix="/categories", tags=["分类"])


@router.get("", response_model=Response[list[CategoryResponse]])
async def list_categories(session: DBSession):
    service = CategoryService(session)
    data = await service.get_all()
    return Response(data=data)


@router.get("/{category_id}", response_model=Response[CategoryResponse])
async def get_category(category_id: int, session: DBSession):
    service = CategoryService(session)
    data = await service.get_by_id(category_id)
    return Response(data=data)


@router.post("", response_model=Response[CategoryResponse], status_code=201)
async def create_category(
    body: CategoryCreate,
    session: DBSession,
    _: CurrentUserID,
):
    service = CategoryService(session)
    data = await service.create(body)
    return Response(data=data)


@router.put("/{category_id}", response_model=Response[CategoryResponse])
async def update_category(
    category_id: int,
    body: CategoryUpdate,
    session: DBSession,
    _: CurrentUserID,
):
    service = CategoryService(session)
    data = await service.update(category_id, body)
    return Response(data=data)


@router.delete("/{category_id}", response_model=Response[None])
async def delete_category(
    category_id: int,
    session: DBSession,
    _: CurrentUserID,
):
    service = CategoryService(session)
    await service.delete(category_id)
    return Response(message="删除成功")
