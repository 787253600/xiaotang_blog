"""缓存键命名规范"""


class CacheKeys:
    ARTICLE_DETAIL = "article:detail:{id}"
    ARTICLE_LIST_PAGE = "article:list:page:{page}:size:{size}"
    ARTICLE_CATEGORY_PAGE = "article:category:{cid}:page:{page}:size:{size}"
    ARTICLE_TAG_PAGE = "article:tag:{tid}:page:{page}:size:{size}"
    CATEGORY_LIST = "category:list"
    TAG_LIST = "tag:list"
    SEARCH_RESULT = "search:{query_hash}"
    JWT_BLACKLIST = "jwt:blacklist:{jti}"

    @staticmethod
    def article_detail(article_id: int) -> str:
        return f"article:detail:{article_id}"

    @staticmethod
    def article_list_page(page: int, size: int) -> str:
        return f"article:list:page:{page}:size:{size}"

    @staticmethod
    def article_category_page(category_id: int, page: int, size: int) -> str:
        return f"article:category:{category_id}:page:{page}:size:{size}"

    @staticmethod
    def article_tag_page(tag_id: int, page: int, size: int) -> str:
        return f"article:tag:{tag_id}:page:{page}:size:{size}"

    @staticmethod
    def search_result(query_hash: str) -> str:
        return f"search:{query_hash}"

    @staticmethod
    def jwt_blacklist(jti: str) -> str:
        return f"jwt:blacklist:{jti}"


class CacheTTL:
    ARTICLE_DETAIL = 3600
    ARTICLE_LIST = 1800
    CATEGORY_LIST = 7200
    TAG_LIST = 7200
    SEARCH_RESULT = 1800


async def redis_get(key: str):
    """安全读取，Redis 不可用时返回 None"""
    from app.cache.client import get_redis_client
    redis = await get_redis_client()
    if redis is None:
        return None
    try:
        return await redis.get(key)
    except Exception:
        return None


async def redis_setex(key: str, ttl: int, value: str) -> None:
    """安全写入，Redis 不可用时静默跳过"""
    from app.cache.client import get_redis_client
    redis = await get_redis_client()
    if redis is None:
        return
    try:
        await redis.setex(key, ttl, value)
    except Exception:
        pass


async def redis_delete(*keys: str) -> None:
    """安全删除，Redis 不可用时静默跳过"""
    from app.cache.client import get_redis_client
    redis = await get_redis_client()
    if redis is None:
        return
    try:
        await redis.delete(*keys)
    except Exception:
        pass
