"""分页参数"""

from fastapi import Query

from app.config import get_settings


class PaginationParams:
    """分页查询参数依赖注入"""

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="页码"),
        page_size: int = Query(default=None, ge=1, description="每页数量"),
    ):
        settings = get_settings()
        self.page = page
        self.page_size = page_size or settings.default_page_size
        if self.page_size > settings.max_page_size:
            self.page_size = settings.max_page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
