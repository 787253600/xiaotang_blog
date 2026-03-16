"""评论 ORM 模型（支持树形嵌套，parent_id 自引用）"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True,
        comment="父评论 ID，NULL 为顶层评论"
    )

    # 游客信息（无需登录）
    author_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="评论者昵称")
    author_email: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="评论者邮箱（不公开）"
    )
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="评论内容")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # 关系
    article: Mapped["Article"] = relationship("Article", back_populates="comments")  # noqa: F821
    parent: Mapped["Comment | None"] = relationship(
        "Comment", remote_side="Comment.id", back_populates="replies"
    )
    replies: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="parent", cascade="all, delete-orphan"
    )
