"""FastAPI 应用入口 - 注册路由、中间件、生命周期"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.cache.client import close_redis_client, get_redis_client
from app.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.db.base import engine
from app.domains.articles.router import router as articles_router
from app.domains.auth.router import router as auth_router
from app.domains.categories.router import router as categories_router
from app.domains.comments.router import router as comments_router
from app.domains.tags.router import router as tags_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 全局异常处理
    register_exception_handlers(app)

    # 注册路由
    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(articles_router, prefix=api_prefix)
    app.include_router(categories_router, prefix=api_prefix)
    app.include_router(tags_router, prefix=api_prefix)
    app.include_router(comments_router, prefix=api_prefix)

    @app.on_event("startup")
    async def startup() -> None:
        logger.info("应用启动中...")
        # 预热 Redis 连接
        await get_redis_client()
        # 检测全文搜索配置
        from app.db.session import get_db
        from app.search.postgres_search import detect_ts_config
        async for session in get_db():
            await detect_ts_config(session)
            break
        logger.info("应用启动完成")

    @app.on_event("shutdown")
    async def shutdown() -> None:
        logger.info("应用关闭中...")
        await close_redis_client()
        await engine.dispose()
        logger.info("应用已关闭")

    @app.get("/health", tags=["系统"])
    async def health_check() -> dict:
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
