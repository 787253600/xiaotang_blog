"""图片上传接口集成测试"""

import pytest

# 最小合法的 PNG 文件（1×1 像素）
VALID_PNG = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02"
    b"\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)

# 最小合法的 JPEG 文件头
VALID_JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 100

# 伪装成 PNG 的纯文本内容（magic bytes 不对）
FAKE_PNG = b"Not a real PNG file content here"


@pytest.fixture
async def auth_headers(client):
    """创建测试用户并返回认证头"""
    await client.post(
        "/api/v1/auth/register",
        json={"username": "uploader", "email": "upload@test.com", "password": "pass123456"},
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"username": "uploader", "password": "pass123456"},
    )
    token = login_res.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_upload_requires_auth(client):
    """未登录时上传应返回 401"""
    response = await client.post(
        "/api/v1/upload/image",
        files={"file": ("test.png", VALID_PNG, "image/png")},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_valid_png(client, auth_headers, tmp_path, monkeypatch):
    """有效 PNG 文件上传成功，返回 url 和 filename"""
    # 将上传目录重定向到临时目录，避免污染真实 static/
    from pathlib import Path
    import app.domains.upload.storage as storage_mod
    monkeypatch.setattr(storage_mod, "UPLOAD_DIR", tmp_path)

    response = await client.post(
        "/api/v1/upload/image",
        files={"file": ("test.png", VALID_PNG, "image/png")},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "url" in data
    assert "filename" in data
    assert data["filename"].endswith(".png")


@pytest.mark.asyncio
async def test_upload_rejects_non_image(client, auth_headers):
    """非图片 Content-Type 应返回 415"""
    response = await client.post(
        "/api/v1/upload/image",
        files={"file": ("test.txt", b"hello world", "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 415


@pytest.mark.asyncio
async def test_upload_rejects_oversized_file(client, auth_headers):
    """超过 5 MB 的文件应返回 413"""
    big_content = b"\xff\xd8\xff" + b"\x00" * (5 * 1024 * 1024 + 1)
    response = await client.post(
        "/api/v1/upload/image",
        files={"file": ("big.jpg", big_content, "image/jpeg")},
        headers=auth_headers,
    )
    assert response.status_code == 413


@pytest.mark.asyncio
async def test_upload_rejects_magic_bytes_mismatch(client, auth_headers):
    """Content-Type 声明为 PNG 但内容不是真实 PNG，应返回 415"""
    response = await client.post(
        "/api/v1/upload/image",
        files={"file": ("fake.png", FAKE_PNG, "image/png")},
        headers=auth_headers,
    )
    assert response.status_code == 415
