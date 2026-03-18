"""统计模块 Pydantic 模式"""

from datetime import date

from pydantic import BaseModel


class DailyVisitItem(BaseModel):
    date: date
    count: int


class OverviewData(BaseModel):
    total_articles: int
    draft_articles: int
    total_views: int
    pending_comments: int
    daily_visits: list[DailyVisitItem]


class OverviewResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: OverviewData
