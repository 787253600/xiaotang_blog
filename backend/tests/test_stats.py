"""统计接口集成测试"""

import pytest


@pytest.mark.asyncio
async def test_overview_requires_auth(client):
    """未登录时访问统计接口应返回 401"""
    response = await client.get("/api/v1/stats/overview")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_overview_returns_structure(client, session):
    """登录后返回正确的数据结构"""
    # 先注册并登录
    await client.post(
        "/api/v1/auth/register",
        json={"username": "stats_user", "email": "stats@test.com", "password": "pass123456"},
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"username": "stats_user", "password": "pass123456"},
    )
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/stats/overview", headers=headers)
    assert response.status_code == 200

    data = response.json()["data"]
    assert "total_articles" in data
    assert "draft_articles" in data
    assert "total_views" in data
    assert "pending_comments" in data
    assert "daily_visits" in data
    assert isinstance(data["daily_visits"], list)


@pytest.mark.asyncio
async def test_overview_daily_visits_always_14_days(client, session):
    """即使没有任何访问记录，也应返回 14 天的数据点"""
    await client.post(
        "/api/v1/auth/register",
        json={"username": "stats_user2", "email": "stats2@test.com", "password": "pass123456"},
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"username": "stats_user2", "password": "pass123456"},
    )
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/stats/overview", headers=headers)
    assert response.status_code == 200
    daily = response.json()["data"]["daily_visits"]
    assert len(daily) == 14
    # 每个元素都有 date 和 count 字段
    for item in daily:
        assert "date" in item
        assert "count" in item
        assert item["count"] >= 0


@pytest.mark.asyncio
async def test_overview_counts_articles_correctly(client, session):
    """总文章数和草稿数计算正确"""
    await client.post(
        "/api/v1/auth/register",
        json={"username": "stats_user3", "email": "stats3@test.com", "password": "pass123456"},
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"username": "stats_user3", "password": "pass123456"},
    )
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 创建 2 篇文章：1 已发布 + 1 草稿
    await client.post(
        "/api/v1/articles",
        json={"title": "Published", "slug": "published-stats", "content": "hello", "is_published": True},
        headers=headers,
    )
    await client.post(
        "/api/v1/articles",
        json={"title": "Draft", "slug": "draft-stats", "content": "hello", "is_published": False},
        headers=headers,
    )

    response = await client.get("/api/v1/stats/overview", headers=headers)
    data = response.json()["data"]
    assert data["total_articles"] >= 2
    assert data["draft_articles"] >= 1
