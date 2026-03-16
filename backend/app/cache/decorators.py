"""缓存装饰器 - 基于 Redis 的函数结果缓存"""

import functools
import hashlib
import json
import logging
from collections.abc import Callable
from typing import Any

from app.cache.client import get_redis_client

logger = logging.getLogger(__name__)


def cached(key: str, ttl: int = 300):
    """
    Redis 缓存装饰器。

    Args:
        key: 缓存键，支持 {参数名} 格式化占位符
        ttl: 缓存过期时间（秒），默认 5 分钟
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            redis = await get_redis_client()

            # 构建缓存键
            try:
                cache_key = key.format(**kwargs)
            except KeyError:
                # 占位符无法填充时，使用参数哈希
                args_hash = hashlib.md5(
                    json.dumps([str(a) for a in args] + [str(kwargs)]).encode()
                ).hexdigest()[:8]
                cache_key = f"{key}:{args_hash}"

            # 尝试读取缓存
            try:
                cached_value = await redis.get(cache_key)
                if cached_value is not None:
                    return json.loads(cached_value)
            except Exception as e:
                logger.warning("Redis 读取失败，跳过缓存: %s", e)

            # 执行原始函数
            result = await func(*args, **kwargs)

            # 写入缓存
            try:
                if result is not None:
                    await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            except Exception as e:
                logger.warning("Redis 写入失败: %s", e)

            return result

        return wrapper

    return decorator
