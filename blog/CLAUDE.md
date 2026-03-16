# blog 模块文档

[根目录](../CLAUDE.md) > **blog**

---

## 模块职责

`blog` 是小唐博客系统的核心 Django 应用，负责：

- 文章（Article/Post）的创建、展示、编辑、删除
- 文章分类（Category）管理
- 文章标签（Tag）管理
- 博客首页与文章详情页的视图渲染
- 管理后台内容管理界面

---

## 入口与启动

本模块由 Django 框架自动加载，通过项目配置中的 `INSTALLED_APPS` 注册：

```python
# xiaotangblog/settings.py
INSTALLED_APPS = [
    ...
    'blog',
]
```

路由挂载点（在根 `urls.py` 中配置）：

```python
# xiaotangblog/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
]
```

---

## 对外接口（预期 URL 路由）

| URL 路径 | 视图名称 | 说明 |
|----------|----------|------|
| `/` | `ArticleListView` | 博客首页，文章列表（分页） |
| `/article/<int:pk>/` | `ArticleDetailView` | 文章详情页 |
| `/category/<slug>/` | `CategoryListView` | 按分类筛选文章 |
| `/tag/<slug>/` | `TagListView` | 按标签筛选文章 |
| `/search/` | `SearchView` | 全文搜索 |
| `/about/` | `AboutView` | 关于页面 |

---

## 数据模型（预期设计）

根据参考环境中 `new_blah.css` 的 CSS 类名（`.articles`、`.meta-cate`、`.rate`、`.rate-score`、`.description`），推断如下数据模型结构：

### Article（文章）

```python
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='正文')
    summary = models.TextField(verbose_name='摘要', blank=True)
    cover = models.ImageField(upload_to='covers/', verbose_name='封面图', blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                  null=True, verbose_name='分类')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    rate_score = models.FloatField(default=0, verbose_name='评分')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章列表'
```

### Category（分类）

```python
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    slug = models.SlugField(unique=True, verbose_name='URL 标识')
    description = models.TextField(blank=True, verbose_name='描述')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类列表'
```

### Tag（标签）

```python
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名称')
    slug = models.SlugField(unique=True, verbose_name='URL 标识')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签列表'
```

---

## 关键依赖与配置

### Python 包依赖

| 包名 | 用途 | 是否必须 |
|------|------|----------|
| Django | Web 框架核心 | 是 |
| Pillow | 图片上传/处理（封面图） | 可选 |

### 模板上下文

主要模板变量：
- `articles` - 文章 QuerySet（列表页）
- `article` - 单篇文章对象（详情页）
- `categories` - 分类列表（侧边栏）
- `page_obj` - Django Paginator 分页对象

---

## 测试与质量

### 测试文件位置

```
blog/tests.py        # 主测试文件
```

### 推荐测试覆盖点

```python
# 模型测试
class ArticleModelTest(TestCase):
    def test_article_str(self): ...
    def test_article_ordering(self): ...

# 视图测试
class ArticleListViewTest(TestCase):
    def test_list_page_returns_200(self): ...
    def test_article_appears_in_list(self): ...

class ArticleDetailViewTest(TestCase):
    def test_detail_page_returns_200(self): ...
    def test_404_for_nonexistent_article(self): ...
```

### 运行测试

```bash
# 仅测试 blog 模块
python manage.py test blog

# 详细输出
python manage.py test blog --verbosity=2
```

---

## 常见问题 (FAQ)

**Q: 修改模型后如何更新数据库？**
```bash
python manage.py makemigrations blog
python manage.py migrate
```

**Q: 如何在管理后台管理文章？**
在 `admin.py` 中注册模型：
```python
from django.contrib import admin
from .models import Article, Category, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'views']
    list_filter = ['category', 'tags', 'created_at']
    search_fields = ['title', 'content']
```

**Q: 参考环境的 CSS 样式如何迁移到本项目？**
将 `../Django/djangoProject/static/new_blah.css` 复制至本项目 `static/css/` 目录，并在 `settings.py` 中配置 `STATICFILES_DIRS`。

---

## 相关文件清单

| 文件路径 | 说明 | 状态 |
|----------|------|------|
| `blog/models.py` | 数据模型定义 | 待创建 |
| `blog/views.py` | 视图逻辑 | 待创建 |
| `blog/urls.py` | URL 路由配置 | 待创建 |
| `blog/admin.py` | 管理后台注册 | 待创建 |
| `blog/tests.py` | 单元测试 | 待创建 |
| `blog/apps.py` | 应用配置 | 待创建 |
| `blog/migrations/` | 数据库迁移文件目录 | 待创建 |
| `blog/templates/blog/` | 应用模板目录 | 待创建 |

---

## 变更记录 (Changelog)

| 版本 | 日期 | 说明 |
|------|------|------|
| 0.1.0 | 2026-03-16 | 模块文档初始化（预期设计，源码待创建） |
