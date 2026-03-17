"""缓存装饰器 - Redis 不可用时透明降级"""

import functools
import hashlib
import json
import logging
from collections.abc import Callable
from typing import Any

from app.cache.client import get_redis_client

logger = logging.getLogger(__name__)


def cached(key: str, ttl: int = 300):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            redis = await get_redis_client()

            if redis is None:
                # Redis 不可用，直接执行原函数
                return await func(*args, **kwargs)

            try:
                cache_key = key.format(**kwargs)
            except KeyError:
                args_hash = hashlib.md5(
                    json.dumps([str(a) for a in args] + [str(kwargs)]).encode()
                ).hexdigest()[:8]
                cache_key = f"{key}:{args_hash}"

            try:
                cached_value = await redis.get(cache_key)
                if cached_value is not None:
                    return json.loads(cached_value)
            except Exception as e:
                logger.warning("Redis 读取失败：%s", e)

            result = await func(*args, **kwargs)

            try:
                if result is not None:
                    await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            except Exception as e:
                logger.warning("Redis 写入失败：%s", e)

            return result

        return wrapper
    return decorator
