"""分类数据访问层"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.categories.models import Category
from app.domains.categories.schemas import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Category]:
        result = await self._session.execute(
            select(Category).order_by(Category.name)
        )
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self._session.get(Category, category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self._session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def update(self, category: Category, data: CategoryUpdate) -> Category:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(category, field, value)
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self._session.delete(category)
        await self._session.flush()

    async def get_article_count(self, category_id: int) -> int:
        from app.domains.articles.models import Article
        result = await self._session.execute(
            select(func.count())
            .select_from(Article)
            .where(Article.category_id == category_id)
            .where(Article.is_published.is_(True))
        )
        return result.scalar() or 0
