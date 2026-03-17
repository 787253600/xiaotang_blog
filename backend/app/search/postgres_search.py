"""PostgreSQL tsvector 全文搜索实现"""

import hashlib
import json
import logging

from sqlalchemy import Select, func, or_, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.client import get_redis_client
from app.cache.keys import CacheTTL, CacheKeys

logger = logging.getLogger(__name__)

# 优先使用 zhparser 中文分词，不可用时降级为 simple
_TS_CONFIG = "simple"  # 运行时由 detect_ts_config() 覆盖


async def detect_ts_config(session: AsyncSession) -> str:
    """检测 PostgreSQL 是否安装 zhparser，返回可用的分词配置名"""
    global _TS_CONFIG
    try:
        result = await session.execute(
            text("SELECT cfgname FROM pg_ts_config WHERE cfgname = 'zhparser'")
        )
        if result.scalar():
            _TS_CONFIG = "zhparser"
            logger.info("全文搜索：使用 zhparser 中文分词")
        else:
            _TS_CONFIG = "simple"
            logger.info("全文搜索：zhparser 不可用，降级为 simple 配置")
    except Exception as e:
        _TS_CONFIG = "simple"
        logger.warning("检测 ts_config 失败，使用 simple: %s", e)
    return _TS_CONFIG


def build_search_query(query_str: str) -> str:
    """
    将用户输入转换为 tsquery 格式。
    多个词之间用 & 连接（AND 逻辑），支持前缀匹配。
    """
    # 清理输入，防止注入
    words = [w.strip() for w in query_str.split() if w.strip()]
    if not words:
        return ""
    # 使用前缀匹配（:*）提升召回率
    return " & ".join(f"{w}:*" for w in words)


async def full_text_search(
    session: AsyncSession,
    model,
    query_str: str,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    """
    执行文章搜索（ILIKE 模糊匹配，支持中文）。

    Args:
        session: 数据库会话
        model: SQLAlchemy 模型（Article）
        query_str: 用户搜索词
        page: 页码
        page_size: 每页数量

    Returns:
        {"items": [...], "total": int}
    """
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    if not query_str.strip():
        return {"items": [], "total": 0}

    pattern = f"%{query_str.strip()}%"

    stmt = (
        select(model)
        .options(
            selectinload(model.category),
            selectinload(model.tags),
        )
        .where(
            model.is_published.is_(True),
            or_(
                model.title.ilike(pattern),
                model.excerpt.ilike(pattern),
                model.content.ilike(pattern),
            ),
        )
        .order_by(model.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    count_stmt = (
        select(func.count())
        .select_from(model)
        .where(
            model.is_published.is_(True),
            or_(
                model.title.ilike(pattern),
                model.excerpt.ilike(pattern),
                model.content.ilike(pattern),
            ),
        )
    )

    result = await session.execute(stmt)
    count_result = await session.execute(count_stmt)

    items = list(result.scalars().all())
    total = count_result.scalar() or 0

    return {"items": items, "total": total}
