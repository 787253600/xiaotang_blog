"""统计路由 /api/v1/stats"""

from fastapi import APIRouter

from app.dependencies import CurrentUserID, DBSession
from app.domains.stats.schemas import OverviewResponse
from app.domains.stats.service import get_overview

router = APIRouter(prefix="/stats", tags=["统计"])


@router.get("/overview", response_model=OverviewResponse)
async def stats_overview(session: DBSession, _: CurrentUserID) -> OverviewResponse:
    """获取仪表盘概览（需登录）"""
    data = await get_overview(session)
    return OverviewResponse(data=data)
