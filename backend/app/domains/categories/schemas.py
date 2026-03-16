"""分类 Pydantic 模式"""

from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=120, pattern=r"^[a-z0-9-]+$")
    description: str | None = Field(None, max_length=500)


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    slug: str | None = Field(None, min_length=1, max_length=120, pattern=r"^[a-z0-9-]+$")
    description: str | None = Field(None, max_length=500)


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    created_at: datetime
    article_count: int = 0

    model_config = {"from_attributes": True}
