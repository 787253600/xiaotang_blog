"""图片上传路由 /api/v1/upload"""

import logging

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.dependencies import CurrentUserID
from app.domains.upload.storage import (
    ALLOWED_CONTENT_TYPES,
    MAX_FILE_SIZE,
    get_storage,
    validate_magic_bytes,
)
from app.schemas.response import Response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/upload", tags=["上传"])


@router.post("/image", response_model=Response[dict])
async def upload_image(
    file: UploadFile,
    _: CurrentUserID,
) -> Response[dict]:
    """上传图片（需登录），返回可访问的 URL。"""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"不支持的文件类型：{file.content_type}，仅允许 JPEG/PNG/GIF/WebP",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="文件超过 5 MB 限制",
        )

    # 验证文件内容 magic bytes，防止 Content-Type 欺骗
    if not validate_magic_bytes(content, file.content_type or ""):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="文件内容与声明的类型不符，请上传真实的图片文件",
        )

    storage = get_storage()
    try:
        url, filename = await storage.save(content, file.content_type, file.filename or "upload")
    except OSError as e:
        logger.error("图片保存失败（磁盘错误）: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="图片保存失败，请联系管理员",
        ) from e

    logger.info("图片上传成功: filename=%s size=%d", filename, len(content))
    return Response(data={"url": url, "filename": filename})
