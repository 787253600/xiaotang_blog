"""文章 ORM 模型（含 tsvector 全文搜索字段）"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domains.tags.models import article_tags


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, comment="文章标题")
    slug: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False, comment="URL 友好标识"
    )
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="Markdown 正文")
    excerpt: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="文章摘要（自动截取或手动填写）"
    )

    # 外键
    category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    # 统计
    view_count: Mapped[int] = mapped_column(Integer, default=0, comment="浏览量")
    like_count: Mapped[int] = mapped_column(Integer, default=0, comment="点赞数")

    # 状态
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="是否已发布"
    )

    # 全文搜索向量（PostgreSQL 触发器自动维护）
    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR, nullable=True, comment="全文搜索向量"
    )

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="发布时间"
    )

    # 关系
    category: Mapped["Category"] = relationship(  # noqa: F821
        "Category", back_populates="articles"
    )
    tags: Mapped[list["Tag"]] = relationship(  # noqa: F821
        "Tag", secondary=article_tags, back_populates="articles"
    )
    comments: Mapped[list["Comment"]] = relationship(  # noqa: F821
        "Comment", back_populates="article", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # 复合索引：已发布 + 时间倒序（列表页核心查询）
        Index("ix_articles_published_created", "is_published", "created_at"),
        # GIN 索引：全文搜索必备
        Index("ix_articles_search_vector", "search_vector", postgresql_using="gin"),
    )
