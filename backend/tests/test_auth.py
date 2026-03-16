"""认证接口集成测试"""

import pytest


@pytest.mark.asyncio
async def test_login_with_wrong_credentials(client):
    """错误的用户名/密码应返回 401"""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_without_token(client):
    """未携带 token 时 /auth/me 应返回 401"""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
