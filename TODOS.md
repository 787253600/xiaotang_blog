# TODOS

## P2 — 文章级别分析统计

**What:** 在仪表盘新增「本周最热文章 Top 5」列表，按 `view_count` 降序排列，显示标题和浏览量。

**Why:** 每篇文章已有 `view_count` 字段，但仪表盘目前只展示全站总量。知道哪篇文章最受欢迎，有助于规划后续内容方向。

**Pros:** 零新 DB 字段，只需一条聚合查询 + 前端列表展示。

**Cons:** 需修改 `stats/service.py`、`stats/schemas.py`，以及 `DashboardView.vue`。

**Context:** `Article.view_count` 在每次调用 `GET /api/v1/articles/{id}` 时由 `ArticleService.increment_view()` 递增。`get_overview()` 已有 DB session，加一条 `select(Article.title, Article.view_count).order_by(desc).limit(5)` 即可。从 `DashboardView.vue` 的 `statCards` 数组下方新增一个列表区块。

**Effort:** S
**Depends on:** 无

---

## P2 — 云端对象存储实现（OSS/S3/COS/R2）

**What:** 实现 `OSSStorageBackend`（或 `S3StorageBackend`），通过 `.env` 中的 `STORAGE_BACKEND=oss` 切换。

**Why:** 当前图片上传到本地 `static/uploads/`，服务器重新部署或迁移时图片会丢失。云存储可以永久保存资源并通过 CDN 加速。

**Pros:** `StorageBackend` 抽象层已建好，路由层零修改；切换完全由工厂函数 `get_storage()` 控制。

**Cons:** 需要引入云存储 SDK（`oss2` / `aiobotocore`），需配置 IAM 权限和 Bucket 策略。

**Context:** `backend/app/domains/upload/storage.py` 中 `get_storage()` 工厂函数已预留扩展点。`.env` 变量已在 `app/config.py` 中定义（`oss_bucket`, `oss_region`, `oss_access_key`, `oss_secret_key`, `oss_cdn_url`）。国内首选阿里云 OSS，国际/自建首选 Cloudflare R2（免费出站流量）。

**Effort:** M
**Depends on:** 无（本地存储可无限期使用）
