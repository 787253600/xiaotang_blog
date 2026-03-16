"""标签数据访问层"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.tags.models import Tag, article_tags
from app.domains.tags.schemas import TagCreate, TagUpdate


class TagRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Tag]:
        result = await self._session.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())

    async def get_by_id(self, tag_id: int) -> Tag | None:
        return await self._session.get(Tag, tag_id)

    async def get_by_slug(self, slug: str) -> Tag | None:
        result = await self._session.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[int]) -> list[Tag]:
        result = await self._session.execute(select(Tag).where(Tag.id.in_(ids)))
        return list(result.scalars().all())

    async def create(self, data: TagCreate) -> Tag:
        tag = Tag(**data.model_dump())
        self._session.add(tag)
        await self._session.flush()
        await self._session.refresh(tag)
        return tag

    async def update(self, tag: Tag, data: TagUpdate) -> Tag:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(tag, field, value)
        await self._session.flush()
        await self._session.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self._session.delete(tag)
        await self._session.flush()

    async def get_article_count(self, tag_id: int) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(article_tags)
            .where(article_tags.c.tag_id == tag_id)
        )
        return result.scalar() or 0
