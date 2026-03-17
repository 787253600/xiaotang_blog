"""友情链接 ORM模型"""
from datetime import datetime

from sqlalchemy import DateTime, String,func
from sqlalchemy.orm import Mapped,mapped_column

from app.db.base import Base

#定义links表进行处理
class Link(Base):
    """
      解释：
  - id: Mapped[int] — 这个字段是整数类型
  - primary_key=True — 它是主键（每条记录的唯一标识）
  - autoincrement=True — 新增记录时自动 +1，不用手动填
    """
    __tablename__ = 'link'
    id:Mapped[int] = mapped_column(primary_key=True,
                                   autoincrement=True)
    name:Mapped[str] = mapped_column(String(100),nullable=False,
                                     comment="网站名称")
    url:Mapped[str] = mapped_column(String(500),nullable=False,
                                    comment="链接地址")
    description:Mapped[str| None] = mapped_column(String(200),nullable=True,
                                                  comment="简介")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())