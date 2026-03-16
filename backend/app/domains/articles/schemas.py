"""文章 Pydantic 模式"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.domains.categories.schemas import CategoryResponse
from app.domains.tags.schemas import TagResponse


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    slug: str = Field(..., min_length=1, max_length=320, pattern=r"^[a-z0-9-]+$")
    content: str = Field(..., min_length=1)
    excerpt: str | None = Field(None, max_length=500)
    category_id: int | None = None
    tag_ids: list[int] = Field(default_factory=list)
    is_published: bool = False


class ArticleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=300)
    slug: str | None = Field(None, min_length=1, max_length=320, pattern=r"^[a-z0-9-]+$")
    content: str | None = Field(None, min_length=1)
    excerpt: str | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None
    is_published: bool | None = None


class ArticleSummary(BaseModel):
    """文章列表摘要（不含完整正文）"""
    id: int
    title: str
    slug: str
    excerpt: str | None
    category: CategoryResponse | None
    tags: list[TagResponse]
    view_count: int
    like_count: int
    is_published: bool
    created_at: datetime
    published_at: datetime | None

    model_config = {"from_attributes": True}


class ArticleResponse(ArticleSummary):
    """文章详情（含完整正文）"""
    content: str
    updated_at: datetime
