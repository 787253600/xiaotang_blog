"""文章业务逻辑层（含缓存失效策略）"""

import json
import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.keys import CacheKeys, CacheTTL, redis_delete, redis_get, redis_setex
from app.cache.client import get_redis_client
from app.core.exceptions import ConflictError, NotFoundError
from app.domains.articles.repository import ArticleRepository
from app.domains.articles.schemas import (
    ArticleCreate,
    ArticleResponse,
    ArticleSummary,
    ArticleUpdate,
)
from app.schemas.pagination import PaginationParams
from app.schemas.response import PaginatedResponse


class ArticleService:
    def __init__(self, session: AsyncSession):
        self._repo = ArticleRepository(session)

    async def get_list(
        self,
        pagination: PaginationParams,
        category_id: int | None = None,
        tag_id: int | None = None,
        published_only: bool = True,
    ) -> PaginatedResponse[ArticleSummary]:
        if category_id:
            cache_key = CacheKeys.article_category_page(
                category_id, pagination.page, pagination.page_size
            )
        elif tag_id:
            cache_key = CacheKeys.article_tag_page(
                tag_id, pagination.page, pagination.page_size
            )
        else:
            cache_key = CacheKeys.article_list_page(pagination.page, pagination.page_size)

        cached = await redis_get(cache_key)
        if cached:
            return PaginatedResponse[ArticleSummary](**json.loads(cached))

        articles, total = await self._repo.get_list(
            offset=pagination.offset,
            limit=pagination.page_size,
            category_id=category_id,
            tag_id=tag_id,
            published_only=published_only,
        )

        result = PaginatedResponse[ArticleSummary](
            items=[ArticleSummary.model_validate(a) for a in articles],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=math.ceil(total / pagination.page_size) if total > 0 else 0,
        )

        await redis_setex(
            cache_key,
            CacheTTL.ARTICLE_LIST,
            json.dumps(result.model_dump(mode="json")),
        )
        return result

    async def get_detail(self, article_id: int, increment_view: bool = False) -> ArticleResponse:
        cache_key = CacheKeys.article_detail(article_id)
        cached = await redis_get(cache_key)
        if cached:
            if increment_view:
                await self._repo.increment_view_count(article_id)
            return ArticleResponse(**json.loads(cached))

        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")

        # 先序列化（model_validate 在 increment 之前，避免 updated_at 被标记过期
        # 后 Pydantic 同步读取触发 MissingGreenlet）
        result = ArticleResponse.model_validate(article)
        await redis_setex(
            cache_key,
            CacheTTL.ARTICLE_DETAIL,
            json.dumps(result.model_dump(mode="json")),
        )

        if increment_view:
            await self._repo.increment_view_count(article_id)

        return result

    async def create(self, data: ArticleCreate) -> ArticleResponse:
        existing = await self._repo.get_by_slug(data.slug)
        if existing:
            raise ConflictError(f"slug '{data.slug}' 已存在")
        article = await self._repo.create(data)
        await self._invalidate_list_cache()
        return ArticleResponse.model_validate(article)

    async def update(self, article_id: int, data: ArticleUpdate) -> ArticleResponse:
        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")
        if data.slug and data.slug != article.slug:
            existing = await self._repo.get_by_slug(data.slug)
            if existing:
                raise ConflictError(f"slug '{data.slug}' 已存在")
        article = await self._repo.update(article, data)
        await self._invalidate_article_cache(article_id)
        return ArticleResponse.model_validate(article)

    async def delete(self, article_id: int) -> None:
        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")
        await self._repo.delete(article)
        await self._invalidate_article_cache(article_id)

    async def like(self, article_id: int) -> None:
        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")
        await self._repo.increment_like_count(article_id)
        await self._invalidate_article_cache(article_id)

    async def search(
        self, query: str, pagination: PaginationParams
    ) -> PaginatedResponse[ArticleSummary]:
        from app.search.postgres_search import full_text_search
        from app.domains.articles.models import Article

        result = await full_text_search(
            self._repo._session,
            Article,
            query,
            page=pagination.page,
            page_size=pagination.page_size,
        )
        items = [ArticleSummary.model_validate(a) for a in result["items"]]
        total = result["total"]
        return PaginatedResponse[ArticleSummary](
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=math.ceil(total / pagination.page_size) if total > 0 else 0,
        )

    async def _invalidate_article_cache(self, article_id: int) -> None:
        await redis_delete(CacheKeys.article_detail(article_id))
        await self._invalidate_list_cache()

    async def _invalidate_list_cache(self) -> None:
        redis = await get_redis_client()
        if redis is None:
            return
        try:
            patterns = ["article:list:*", "article:category:*", "article:tag:*"]
            for pattern in patterns:
                async for key in redis.scan_iter(pattern):
                    await redis.delete(key)
        except Exception:
            pass
