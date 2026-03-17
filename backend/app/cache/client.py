"""Redis 客户端管理，支持无 Redis 时静默降级"""

import logging

logger = logging.getLogger(__name__)

_redis_client = None
_redis_available = False


async def get_redis_client():
    """
    获取 Redis 客户端。
    若 Redis 不可用，返回 None（调用方需判断）。
    """
    global _redis_client, _redis_available

    if _redis_client is not None:
        return _redis_client

    try:
        from redis.asyncio import Redis
        from app.config import get_settings
        settings = get_settings()
        client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2,
        )
        # 测试连通性
        await client.ping()
        _redis_client = client
        _redis_available = True
        logger.info("Redis 连接成功：%s", settings.redis_url)
    except Exception as e:
        _redis_client = None
        _redis_available = False
        logger.warning("Redis 不可用，缓存已禁用：%s", e)

    return _redis_client


async def close_redis_client() -> None:
    """应用关闭时释放连接"""
    global _redis_client, _redis_available
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
        _redis_available = False
