"""文章数据访问层（CRUD + 搜索 + 分页）"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.articles.models import Article
from app.domains.articles.schemas import ArticleCreate, ArticleUpdate
from app.domains.tags.repository import TagRepository


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._tag_repo = TagRepository(session)

    def _base_query(self) -> select:
        """基础查询：预加载关联数据"""
        return select(Article).options(
            selectinload(Article.category),
            selectinload(Article.tags),
        )

    async def get_list(
        self,
        offset: int,
        limit: int,
        category_id: int | None = None,
        tag_id: int | None = None,
        published_only: bool = True,
    ) -> tuple[list[Article], int]:
        stmt = self._base_query()
        count_stmt = select(func.count()).select_from(Article)

        if published_only:
            stmt = stmt.where(Article.is_published.is_(True))
            count_stmt = count_stmt.where(Article.is_published.is_(True))

        if category_id is not None:
            stmt = stmt.where(Article.category_id == category_id)
            count_stmt = count_stmt.where(Article.category_id == category_id)

        if tag_id is not None:
            from app.domains.tags.models import article_tags
            stmt = stmt.join(article_tags, Article.id == article_tags.c.article_id).where(
                article_tags.c.tag_id == tag_id
            )
            count_stmt = count_stmt.join(
                article_tags, Article.id == article_tags.c.article_id
            ).where(article_tags.c.tag_id == tag_id)

        stmt = stmt.order_by(Article.created_at.desc()).offset(offset).limit(limit)

        result = await self._session.execute(stmt)
        count_result = await self._session.execute(count_stmt)

        return list(result.scalars().all()), count_result.scalar() or 0

    async def get_by_id(self, article_id: int) -> Article | None:
        result = await self._session.execute(
            self._base_query().where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Article | None:
        result = await self._session.execute(
            self._base_query().where(Article.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ArticleCreate) -> Article:
        article_data = data.model_dump(exclude={"tag_ids"})
        article = Article(**article_data)

        if data.tag_ids:
            article.tags = await self._tag_repo.get_by_ids(data.tag_ids)

        # 自动生成摘要
        if not article.excerpt and article.content:
            article.excerpt = article.content[:200].strip()

        self._session.add(article)
        await self._session.flush()
        await self._session.refresh(article, ["category", "tags"])
        return article

    async def update(self, article: Article, data: ArticleUpdate) -> Article:
        update_data = data.model_dump(exclude_none=True, exclude={"tag_ids"})
        for field, value in update_data.items():
            setattr(article, field, value)

        if data.tag_ids is not None:
            article.tags = await self._tag_repo.get_by_ids(data.tag_ids)

        await self._session.flush()
        await self._session.refresh(article, ["category", "tags"])
        return article

    async def delete(self, article: Article) -> None:
        await self._session.delete(article)
        await self._session.flush()

    async def increment_view_count(self, article_id: int) -> None:
        from sqlalchemy import update
        await self._session.execute(
            update(Article)
            .where(Article.id == article_id)
            .values(view_count=Article.view_count + 1)
        )

    async def increment_like_count(self, article_id: int) -> None:
        from sqlalchemy import update
        await self._session.execute(
            update(Article)
            .where(Article.id == article_id)
            .values(like_count=Article.like_count + 1)
        )
