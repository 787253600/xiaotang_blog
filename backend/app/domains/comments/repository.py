"""评论数据访问层"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.comments.models import Comment
from app.domains.comments.schemas import CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_article(self, article_id: int) -> list[Comment]:
        """获取文章所有顶层评论（含嵌套回复）"""
        result = await self._session.execute(
            select(Comment)
            .where(Comment.article_id == article_id)
            .where(Comment.parent_id.is_(None))
            .options(selectinload(Comment.replies).selectinload(Comment.replies))
            .order_by(Comment.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int) -> Comment | None:
        return await self._session.get(Comment, comment_id)

    async def create(self, article_id: int, data: CommentCreate) -> Comment:
        comment = Comment(
            article_id=article_id,
            parent_id=data.parent_id,
            author_name=data.author_name,
            author_email=data.author_email,
            content=data.content,
        )
        self._session.add(comment)
        await self._session.flush()
        await self._session.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)
        await self._session.flush()
