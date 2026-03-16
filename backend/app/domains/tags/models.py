"""标签 ORM 模型"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# 文章-标签关联表（多对多）
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="标签名称"
    )
    slug: Mapped[str] = mapped_column(
        String(60), unique=True, nullable=False, comment="URL 友好标识"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # 反向关系
    articles: Mapped[list["Article"]] = relationship(  # noqa: F821
        "Article", secondary=article_tags, back_populates="tags"
    )
