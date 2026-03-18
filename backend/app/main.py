"""FastAPI 应用入口 - 注册路由、中间件、生命周期"""

import logging
from contextlib import asynccontextmanager
from datetime import date
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.cache.client import close_redis_client, get_redis_client
from app.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.security import hash_password
from app.db.base import AsyncSessionLocal, engine
from app.domains.articles.router import router as articles_router
from app.domains.auth.models import User
from app.domains.auth.router import router as auth_router
from app.domains.categories.router import router as categories_router
from app.domains.comments.router import router as comments_router
from app.domains.links.router import router as links_router
from app.domains.stats.router import router as stats_router
from app.domains.tags.router import router as tags_router
from app.domains.upload.router import router as upload_router
from app.search.postgres_search import detect_ts_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期：启动初始化 → 运行 → 关闭清理"""
    logger.info("应用启动中...")

    # 预热 Redis 连接
    await get_redis_client()

    async with AsyncSessionLocal() as session:
        # 检测全文搜索配置
        await detect_ts_config(session)

        # 自动创建管理员账号（若不存在）
        result = await session.execute(
            select(User).where(User.username == settings.admin_username)
        )
        if result.scalar_one_or_none() is None:
            admin = User(
                username=settings.admin_username,
                email=settings.admin_email,
                hashed_password=hash_password(settings.admin_password),
                is_active=True,
            )
            session.add(admin)
            await session.commit()
            logger.info("管理员账号已初始化: %s", settings.admin_username)
        else:
            logger.info("管理员账号已存在，跳过初始化")

    logger.info("应用启动完成")

    yield  # 应用运行中

    logger.info("应用关闭中...")
    await close_redis_client()
    await engine.dispose()
    logger.info("应用已关闭")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
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
    app.include_router(links_router, prefix=api_prefix)
    app.include_router(stats_router, prefix=api_prefix)
    app.include_router(upload_router, prefix=api_prefix)

    # 静态文件（上传图片等）
    import os
    os.makedirs("static/uploads", exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 访问计数中间件：仅统计文章详情页的真实读取（GET /api/v1/articles/{id}）
    import re as _re
    _article_path_re = _re.compile(r"^/api/v1/articles/\d+$")

    @app.middleware("http")
    async def visit_counter(request: Request, call_next):
        response = await call_next(request)
        if request.method == "GET" and _article_path_re.match(request.url.path):
            try:
                redis = await get_redis_client()
                if redis:
                    key = f"stats:visits:{date.today().isoformat()}"
                    await redis.incr(key)
            except Exception:
                pass
        return response

    @app.get("/health", tags=["系统"])
    async def health_check() -> dict:
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
