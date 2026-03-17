"""每日访问统计 ORM 模型"""

from datetime import date

from sqlalchemy import Date, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DailyVisit(Base):
    __tablename__ = "daily_visits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, comment="统计日期")
    count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="访问次数")

    __table_args__ = (UniqueConstraint("date", name="uq_daily_visits_date"),)
