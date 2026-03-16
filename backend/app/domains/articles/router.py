"""文章路由 /api/v1/articles"""

from fastapi import APIRouter, Depends, Query

from app.dependencies import CurrentUserID, DBSession
from app.domains.articles.schemas import (
    ArticleCreate,
    ArticleResponse,
    ArticleSummary,
    ArticleUpdate,
)
from app.domains.articles.service import ArticleService
from app.schemas.pagination import PaginationParams
from app.schemas.response import PaginatedResponse, Response

router = APIRouter(prefix="/articles", tags=["文章"])


@router.get("", response_model=PaginatedResponse[ArticleSummary])
async def list_articles(
    session: DBSession,
    pagination: PaginationParams = Depends(),
    category_id: int | None = Query(None),
    tag_id: int | None = Query(None),
):
    service = ArticleService(session)
    return await service.get_list(pagination, category_id=category_id, tag_id=tag_id)


@router.get("/search", response_model=PaginatedResponse[ArticleSummary])
async def search_articles(
    session: DBSession,
    q: str = Query(..., min_length=1, description="搜索关键词"),
    pagination: PaginationParams = Depends(),
):
    service = ArticleService(session)
    return await service.search(q, pagination)


@router.get("/{article_id}", response_model=Response[ArticleResponse])
async def get_article(article_id: int, session: DBSession):
    service = ArticleService(session)
    data = await service.get_detail(article_id, increment_view=True)
    return Response(data=data)


@router.post("", response_model=Response[ArticleResponse], status_code=201)
async def create_article(
    body: ArticleCreate,
    session: DBSession,
    _: CurrentUserID,
):
    service = ArticleService(session)
    data = await service.create(body)
    return Response(data=data)


@router.put("/{article_id}", response_model=Response[ArticleResponse])
async def update_article(
    article_id: int,
    body: ArticleUpdate,
    session: DBSession,
    _: CurrentUserID,
):
    service = ArticleService(session)
    data = await service.update(article_id, body)
    return Response(data=data)


@router.delete("/{article_id}", response_model=Response[None])
async def delete_article(
    article_id: int,
    session: DBSession,
    _: CurrentUserID,
):
    service = ArticleService(session)
    await service.delete(article_id)
    return Response(message="删除成功")


@router.post("/{article_id}/likes", response_model=Response[None])
async def like_article(article_id: int, session: DBSession):
    service = ArticleService(session)
    await service.like(article_id)
    return Response(message="点赞成功")
