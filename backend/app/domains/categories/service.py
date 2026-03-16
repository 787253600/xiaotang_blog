"""分类业务逻辑层"""

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.client import get_redis_client
from app.cache.keys import CacheKeys, CacheTTL
from app.core.exceptions import ConflictError, NotFoundError
from app.domains.categories.repository import CategoryRepository
from app.domains.categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


class CategoryService:
    def __init__(self, session: AsyncSession):
        self._repo = CategoryRepository(session)

    async def get_all(self) -> list[CategoryResponse]:
        redis = await get_redis_client()
        cached = await redis.get(CacheKeys.CATEGORY_LIST)
        if cached:
            return [CategoryResponse(**item) for item in json.loads(cached)]

        categories = await self._repo.get_all()
        result = []
        for cat in categories:
            count = await self._repo.get_article_count(cat.id)
            resp = CategoryResponse.model_validate(cat)
            resp.article_count = count
            result.append(resp)

        await redis.setex(
            CacheKeys.CATEGORY_LIST,
            CacheTTL.CATEGORY_LIST,
            json.dumps([r.model_dump(mode="json") for r in result]),
        )
        return result

    async def get_by_id(self, category_id: int) -> CategoryResponse:
        category = await self._repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("分类")
        count = await self._repo.get_article_count(category_id)
        resp = CategoryResponse.model_validate(category)
        resp.article_count = count
        return resp

    async def create(self, data: CategoryCreate) -> CategoryResponse:
        existing = await self._repo.get_by_slug(data.slug)
        if existing:
            raise ConflictError(f"slug '{data.slug}' 已存在")
        category = await self._repo.create(data)
        await self._invalidate_cache()
        return CategoryResponse.model_validate(category)

    async def update(self, category_id: int, data: CategoryUpdate) -> CategoryResponse:
        category = await self._repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("分类")
        if data.slug and data.slug != category.slug:
            existing = await self._repo.get_by_slug(data.slug)
            if existing:
                raise ConflictError(f"slug '{data.slug}' 已存在")
        category = await self._repo.update(category, data)
        await self._invalidate_cache()
        return CategoryResponse.model_validate(category)

    async def delete(self, category_id: int) -> None:
        category = await self._repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("分类")
        await self._repo.delete(category)
        await self._invalidate_cache()

    async def _invalidate_cache(self) -> None:
        redis = await get_redis_client()
        await redis.delete(CacheKeys.CATEGORY_LIST)
