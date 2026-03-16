"""缓存键命名规范 - 统一管理所有缓存键格式"""


class CacheKeys:
    """缓存键常量与生成方法"""

    # 文章
    ARTICLE_DETAIL = "article:detail:{id}"
    ARTICLE_LIST_PAGE = "article:list:page:{page}:size:{size}"
    ARTICLE_CATEGORY_PAGE = "article:category:{cid}:page:{page}:size:{size}"
    ARTICLE_TAG_PAGE = "article:tag:{tid}:page:{page}:size:{size}"

    # 分类/标签
    CATEGORY_LIST = "category:list"
    TAG_LIST = "tag:list"

    # 搜索
    SEARCH_RESULT = "search:{query_hash}"

    # JWT 黑名单
    JWT_BLACKLIST = "jwt:blacklist:{jti}"

    @staticmethod
    def article_detail(article_id: int) -> str:
        return CacheKeys.ARTICLE_DETAIL.format(id=article_id)

    @staticmethod
    def article_list_page(page: int, size: int) -> str:
        return CacheKeys.ARTICLE_LIST_PAGE.format(page=page, size=size)

    @staticmethod
    def article_category_page(category_id: int, page: int, size: int) -> str:
        return CacheKeys.ARTICLE_CATEGORY_PAGE.format(
            cid=category_id, page=page, size=size
        )

    @staticmethod
    def article_tag_page(tag_id: int, page: int, size: int) -> str:
        return CacheKeys.ARTICLE_TAG_PAGE.format(tid=tag_id, page=page, size=size)

    @staticmethod
    def search_result(query_hash: str) -> str:
        return CacheKeys.SEARCH_RESULT.format(query_hash=query_hash)

    @staticmethod
    def jwt_blacklist(jti: str) -> str:
        return CacheKeys.JWT_BLACKLIST.format(jti=jti)


# TTL 常量（秒）
class CacheTTL:
    ARTICLE_DETAIL = 3600        # 1 小时
    ARTICLE_LIST = 1800          # 30 分钟
    CATEGORY_LIST = 7200         # 2 小时
    TAG_LIST = 7200              # 2 小时
    SEARCH_RESULT = 1800         # 30 分钟
