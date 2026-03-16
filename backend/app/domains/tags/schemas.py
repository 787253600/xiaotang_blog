"""标签 Pydantic 模式"""

from datetime import datetime

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=60, pattern=r"^[a-z0-9-]+$")


class TagUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    slug: str | None = Field(None, min_length=1, max_length=60, pattern=r"^[a-z0-9-]+$")


class TagResponse(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime
    article_count: int = 0

    model_config = {"from_attributes": True}
