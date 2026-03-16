"""Redis 客户端单例管理"""

from redis.asyncio import Redis

from app.config import get_settings

_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    """获取 Redis 客户端单例（应用启动时初始化）"""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = Redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis_client() -> None:
    """应用关闭时释放连接"""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
