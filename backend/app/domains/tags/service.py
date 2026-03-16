"""标签业务逻辑层"""

import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.client import get_redis_client
from app.cache.keys import CacheKeys, CacheTTL
from app.core.exceptions import ConflictError, NotFoundError
from app.domains.tags.repository import TagRepository
from app.domains.tags.schemas import TagCreate, TagResponse, TagUpdate


class TagService:
    def __init__(self, session: AsyncSession):
        self._repo = TagRepository(session)

    async def get_all(self) -> list[TagResponse]:
        redis = await get_redis_client()
        cached = await redis.get(CacheKeys.TAG_LIST)
        if cached:
            return [TagResponse(**item) for item in json.loads(cached)]

        tags = await self._repo.get_all()
        result = []
        for tag in tags:
            count = await self._repo.get_article_count(tag.id)
            resp = TagResponse.model_validate(tag)
            resp.article_count = count
            result.append(resp)

        await redis.setex(
            CacheKeys.TAG_LIST,
            CacheTTL.TAG_LIST,
            json.dumps([r.model_dump(mode="json") for r in result]),
        )
        return result

    async def create(self, data: TagCreate) -> TagResponse:
        existing = await self._repo.get_by_slug(data.slug)
        if existing:
            raise ConflictError(f"slug '{data.slug}' 已存在")
        tag = await self._repo.create(data)
        await self._invalidate_cache()
        return TagResponse.model_validate(tag)

    async def update(self, tag_id: int, data: TagUpdate) -> TagResponse:
        tag = await self._repo.get_by_id(tag_id)
        if not tag:
            raise NotFoundError("标签")
        if data.slug and data.slug != tag.slug:
            existing = await self._repo.get_by_slug(data.slug)
            if existing:
                raise ConflictError(f"slug '{data.slug}' 已存在")
        tag = await self._repo.update(tag, data)
        await self._invalidate_cache()
        return TagResponse.model_validate(tag)

    async def delete(self, tag_id: int) -> None:
        tag = await self._repo.get_by_id(tag_id)
        if not tag:
            raise NotFoundError("标签")
        await self._repo.delete(tag)
        await self._invalidate_cache()

    async def _invalidate_cache(self) -> None:
        redis = await get_redis_client()
        await redis.delete(CacheKeys.TAG_LIST)
