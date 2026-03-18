"""统计业务逻辑"""

import logging
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.articles.models import Article
from app.domains.comments.models import Comment
from app.domains.stats.models import DailyVisit
from app.domains.stats.schemas import DailyVisitItem, OverviewData

logger = logging.getLogger(__name__)


async def flush_redis_visits(session: AsyncSession) -> None:
    """将 Redis 中昨日及更早的访问计数刷新到数据库（可在定时任务中调用）。"""
    try:
        from app.cache.client import get_redis_client
        redis = await get_redis_client()
        if redis is None:
            return
        today_key = f"stats:visits:{date.today().isoformat()}"
        keys = await redis.keys("stats:visits:*")
        for key in keys:
            if key == today_key:
                continue  # 当天数据继续累计
            count_str = await redis.get(key)
            if count_str is None:
                continue
            count = int(count_str)
            day = date.fromisoformat(key.split(":")[-1])
            stmt = (
                pg_insert(DailyVisit)
                .values(date=day, count=count)
                .on_conflict_do_update(
                    index_elements=["date"],
                    set_={"count": DailyVisit.count + count},
                )
            )
            await session.execute(stmt)
            await redis.delete(key)
        await session.commit()
    except Exception as e:
        logger.warning("Redis 访问统计刷新失败：%s", e)


async def get_overview(session: AsyncSession) -> OverviewData:
    """获取仪表盘概览数据。"""
    try:
        # 文章统计
        total_articles_result = await session.execute(select(func.count()).select_from(Article))
        total_articles = total_articles_result.scalar_one()

        draft_result = await session.execute(
            select(func.count()).select_from(Article).where(Article.is_published == False)  # noqa: E712
        )
        draft_articles = draft_result.scalar_one()

        # 待处理评论数（所有评论，可按需扩展审核状态字段后过滤）
        comments_result = await session.execute(select(func.count()).select_from(Comment))
        pending_comments = comments_result.scalar_one()

        # 总浏览量（先取 DB 存量）
        total_views_result = await session.execute(select(func.sum(Article.view_count)))
        total_views_db = total_views_result.scalar_one() or 0
    except Exception as e:
        logger.error("stats overview DB 查询失败: %s", e)
        raise

    # Redis 当日实时浏览计数（累加到总量）
    try:
        from app.cache.client import get_redis_client
        redis = await get_redis_client()
        if redis:
            today_key = f"stats:visits:{date.today().isoformat()}"
            today_count_str = await redis.get(today_key)
            total_views_db += int(today_count_str) if today_count_str else 0
    except Exception:
        pass

    # 近 14 天访问量（优先 DB，当天补 Redis）
    today = date.today()
    start = today - timedelta(days=13)

    try:
        db_result = await session.execute(
            select(DailyVisit).where(DailyVisit.date >= start).order_by(DailyVisit.date)
        )
        db_rows = {row.date: row.count for row in db_result.scalars().all()}
    except Exception as e:
        logger.warning("daily_visits 查询失败，使用空数据: %s", e)
        db_rows = {}

    # 补全缺失日期 + 当天 Redis 计数
    daily_visits: list[DailyVisitItem] = []
    for i in range(14):
        day = start + timedelta(days=i)
        count = db_rows.get(day, 0)
        if day == today:
            try:
                from app.cache.client import get_redis_client
                redis = await get_redis_client()
                if redis:
                    today_key = f"stats:visits:{today.isoformat()}"
                    val = await redis.get(today_key)
                    count = int(val) if val else count
            except Exception:
                pass
        daily_visits.append(DailyVisitItem(date=day, count=count))

    return OverviewData(
        total_articles=total_articles,
        draft_articles=draft_articles,
        total_views=total_views_db,
        pending_comments=pending_comments,
        daily_visits=daily_visits,
    )
