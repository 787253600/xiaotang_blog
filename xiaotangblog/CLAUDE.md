# xiaotangblog 配置包文档

[根目录](../CLAUDE.md) > **xiaotangblog**

---

## 模块职责

`xiaotangblog/` 是 Django 项目的核心配置包，负责：

- 全局 Django 配置（`settings.py`）
- 根 URL 路由分发（`urls.py`）
- WSGI / ASGI 服务器入口
- 项目级中间件、安全、静态文件等配置

---

## 入口与启动

Django 通过 `manage.py` 加载此包：

```python
# manage.py（项目根目录）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaotangblog.settings')
```

WSGI 服务器（生产）入口：

```python
# xiaotangblog/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaotangblog.settings')
application = get_wsgi_application()
```

---

## 对外接口（根路由配置）

```python
# xiaotangblog/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 关键依赖与配置

### settings.py 核心配置说明

| 配置项 | 推荐值（开发）| 说明 |
|--------|--------------|------|
| `DEBUG` | `True` | 生产环境必须设为 `False` |
| `ALLOWED_HOSTS` | `['localhost', '127.0.0.1']` | 生产需配置实际域名 |
| `SECRET_KEY` | 随机字符串 | 必须保密，不得提交到 Git |
| `DATABASES` | SQLite | 生产环境建议 PostgreSQL |
| `STATIC_URL` | `'/static/'` | 静态文件 URL 前缀 |
| `LANGUAGE_CODE` | `'zh-hans'` | 中文界面 |
| `TIME_ZONE` | `'Asia/Shanghai'` | 中国时区 |

### 环境变量管理（推荐）

生产环境建议将敏感配置移至环境变量：

```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-fallback-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
```

---

## 相关文件清单

| 文件路径 | 说明 | 状态 |
|----------|------|------|
| `xiaotangblog/__init__.py` | 包初始化文件 | 待创建 |
| `xiaotangblog/settings.py` | 全局 Django 配置 | 待创建 |
| `xiaotangblog/urls.py` | 根 URL 路由 | 待创建 |
| `xiaotangblog/wsgi.py` | WSGI 服务器入口 | 待创建 |
| `xiaotangblog/asgi.py` | ASGI 服务器入口（异步支持） | 待创建 |
| `manage.py` | Django 命令行工具（项目根） | 待创建 |

---

## 常见问题 (FAQ)

**Q: 如何快速生成此包？**
```bash
# 在项目根目录执行（注意末尾的点，表示当前目录）
django-admin startproject xiaotangblog .
```

**Q: 如何开启中文管理后台？**
在 `settings.py` 中设置：
```python
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True
```

**Q: 生产部署时需要注意什么？**
1. 设置 `DEBUG = False`
2. 配置 `ALLOWED_HOSTS`
3. 运行 `python manage.py collectstatic`
4. 使用 Gunicorn + Nginx 部署 WSGI 应用
5. 将 `SECRET_KEY` 移至环境变量

---

## 变更记录 (Changelog)

| 版本 | 日期 | 说明 |
|------|------|------|
| 0.1.0 | 2026-03-16 | 配置包文档初始化（源码待创建） |
