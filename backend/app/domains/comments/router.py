"""评论路由 /api/v1/articles/{id}/comments"""

from fastapi import APIRouter

from app.dependencies import CurrentUserID, DBSession
from app.domains.comments.schemas import CommentCreate, CommentResponse
from app.domains.comments.service import CommentService
from app.schemas.response import Response

router = APIRouter(prefix="/articles/{article_id}/comments", tags=["评论"])


@router.get("", response_model=Response[list[CommentResponse]])
async def list_comments(article_id: int, session: DBSession):
    service = CommentService(session)
    data = await service.get_by_article(article_id)
    return Response(data=data)


@router.post("", response_model=Response[CommentResponse], status_code=201)
async def create_comment(
    article_id: int,
    body: CommentCreate,
    session: DBSession,
):
    service = CommentService(session)
    data = await service.create(article_id, body)
    return Response(data=data)


@router.delete("/{comment_id}", response_model=Response[None])
async def delete_comment(
    article_id: int,
    comment_id: int,
    session: DBSession,
    _: CurrentUserID,
):
    service = CommentService(session)
    await service.delete(comment_id)
    return Response(message="删除成功")
