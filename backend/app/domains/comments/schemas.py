"""评论 Pydantic 模式"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CommentCreate(BaseModel):
    author_name: str = Field(..., min_length=1, max_length=50)
    author_email: str | None = Field(None, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    article_id: int
    parent_id: int | None
    author_name: str
    content: str
    created_at: datetime
    replies: list[CommentResponse] = []

    model_config = {"from_attributes": True}
