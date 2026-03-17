# 小汤博客 (Xiaotangblog)

基于 **FastAPI + Vue 3** 构建的个人技术博客系统。

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | FastAPI + Uvicorn |
| 数据库 | PostgreSQL 16 + SQLAlchemy 2.x (async) + Alembic |
| 缓存 | Redis 7（可选，不可用时自动降级）|
| 全文搜索 | PostgreSQL tsvector（支持 zhparser 中文分词，自动降级 simple）|
| 前端 | Vue 3 + TypeScript + Vite + Pinia + Vue Router |
| 编辑器 | Vditor（所见即所得 Markdown）|
| 容器化 | Docker + Docker Compose（可选）|

---

## 目录结构

```
Xiaotangblog/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── main.py         # 应用入口
│   │   ├── config.py       # 配置管理（Pydantic Settings）
│   │   ├── dependencies.py # 全局依赖注入
│   │   ├── core/           # 安全（JWT）、异常处理
│   │   ├── db/             # 数据库引擎与会话
│   │   ├── cache/          # Redis 客户端与缓存工具
│   │   ├── search/         # PostgreSQL 全文搜索
│   │   ├── domains/        # 领域模块
│   │   │   ├── articles/   # 文章（CRUD + 搜索 + 缓存）
│   │   │   ├── categories/ # 分类
│   │   │   ├── tags/       # 标签
│   │   │   ├── comments/   # 评论（树形嵌套）
│   │   │   └── auth/       # 登录 / 注销 / JWT 刷新
│   │   └── schemas/        # 统一响应格式
│   ├── migrations/         # Alembic 迁移
│   ├── tests/              # pytest 测试
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/            # axios 封装（自动 token 刷新）
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── router/         # 路由（含管理后台守卫）
│   │   ├── views/          # 页面（public + admin）
│   │   ├── components/     # 公共组件
│   │   └── composables/    # 逻辑复用
│   └── package.json
│
├── docker/                 # Nginx 配置、数据库初始化脚本
├── docker-compose.yml      # 开发环境
├── docker-compose.prod.yml # 生产环境
└── .env.example
```

---

## 本地开发

### 前置要求

- Python 3.12+
- Node.js 18+
- PostgreSQL 16+
- Redis 7+（可选，不安装时缓存自动禁用）

### 后端启动

```powershell
cd backend

# 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
# 编辑 .env，填写数据库连接信息：
# DATABASE_URL=postgresql+asyncpg://用户名:密码@localhost:5432/xiaotangblog

# 生成并执行数据库迁移
alembic revision --autogenerate -m "init"
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 Swagger UI。

### 前端启动

```powershell
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000。

---

## Docker 部署

```bash
# 复制环境变量配置
cp .env.example .env

# 启动开发环境（含热重载）
docker-compose up -d

# 执行数据库迁移
docker-compose exec backend alembic upgrade head
```

### 生产环境

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## API 文档

| 接口 | 说明 |
|------|------|
| `GET /api/v1/articles` | 文章列表（分页 + 分类/标签筛选）|
| `GET /api/v1/articles/{id}` | 文章详情（自动增加浏览量）|
| `GET /api/v1/articles/search?q=` | 全文搜索 |
| `POST /api/v1/articles` | 创建文章（需登录）|
| `PUT /api/v1/articles/{id}` | 更新文章（需登录）|
| `DELETE /api/v1/articles/{id}` | 删除文章（需登录）|
| `GET /api/v1/categories` | 分类列表 |
| `GET /api/v1/tags` | 标签列表 |
| `POST /api/v1/auth/login` | 登录，返回 JWT |
| `POST /api/v1/auth/logout` | 注销（token 加入黑名单）|
| `POST /api/v1/auth/refresh` | 刷新 access token |
| `GET /api/v1/articles/{id}/comments` | 评论列表 |
| `POST /api/v1/articles/{id}/comments` | 发表评论 |

完整文档（开发模式）：http://localhost:8000/docs

---

## 缓存策略

| 缓存键 | TTL | 失效时机 |
|--------|-----|---------|
| `article:detail:{id}` | 1h | 文章更新/删除 |
| `article:list:page:*` | 30min | 任意文章变更 |
| `category:list` | 2h | 分类增删改 |
| `tag:list` | 2h | 标签增删改 |
| `search:{hash}` | 30min | — |
| `jwt:blacklist:{jti}` | 动态 | 注销时写入 |

> Redis 不可用时自动降级为直接查库，功能不受影响。

---

## 常用命令

```powershell
# 生成新迁移
alembic revision --autogenerate -m "描述"

# 回滚迁移
alembic downgrade -1

# 运行测试
pytest

# 代码格式化
black app/
ruff check app/ --fix
```
