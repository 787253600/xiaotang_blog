"""分类 ORM 模型"""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, comment="分类名称"
    )
    slug: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, comment="URL 友好标识"
    )
    description: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="分类描述"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # 反向关系
    articles: Mapped[list["Article"]] = relationship(  # noqa: F821
        "Article", back_populates="category"
    )
