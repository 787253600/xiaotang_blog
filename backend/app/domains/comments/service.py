"""评论业务逻辑层"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domains.articles.repository import ArticleRepository
from app.domains.comments.repository import CommentRepository
from app.domains.comments.schemas import CommentCreate, CommentResponse


class CommentService:
    def __init__(self, session: AsyncSession):
        self._repo = CommentRepository(session)
        self._article_repo = ArticleRepository(session)

    async def get_by_article(self, article_id: int) -> list[CommentResponse]:
        article = await self._article_repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")
        comments = await self._repo.get_by_article(article_id)
        return [CommentResponse.model_validate(c) for c in comments]

    async def create(self, article_id: int, data: CommentCreate) -> CommentResponse:
        article = await self._article_repo.get_by_id(article_id)
        if not article:
            raise NotFoundError("文章")

        if data.parent_id:
            parent = await self._repo.get_by_id(data.parent_id)
            if not parent or parent.article_id != article_id:
                raise NotFoundError("父评论")

        comment = await self._repo.create(article_id, data)
        return CommentResponse.model_validate(comment)

    async def delete(self, comment_id: int) -> None:
        comment = await self._repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundError("评论")
        await self._repo.delete(comment)
