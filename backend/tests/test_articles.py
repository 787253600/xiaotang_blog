"""文章接口集成测试"""

import pytest


@pytest.mark.asyncio
async def test_list_articles_empty(client):
    """空数据库时，文章列表应返回空数组"""
    response = await client.get("/api/v1/articles")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_nonexistent_article(client):
    """访问不存在的文章应返回 404"""
    response = await client.get("/api/v1/articles/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_article_requires_auth(client):
    """未登录时创建文章应返回 401"""
    response = await client.post(
        "/api/v1/articles",
        json={
            "title": "Test",
            "slug": "test",
            "content": "content",
            "is_published": True,
        },
    )
    assert response.status_code == 401
