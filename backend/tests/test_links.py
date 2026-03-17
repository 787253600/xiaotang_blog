"""友情链接接口集成测试"""

import pytest

@pytest.mark.asyncio
async def test_get_links_empty(client):
    """没有数据时返回空列表"""
    respose = await client.get("/api/v1/links")
    assert respose.status_code == 200
    assert respose.json() == []

@pytest.mark.asyncio
async def test_get_links_not_found(client):
    """访问不存在的链接返回 404"""
    response = await client.get("/api/v1/links/9999")
    assert response.status_code == 404