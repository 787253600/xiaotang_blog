"""图片上传路由 /api/v1/upload"""

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.dependencies import CurrentUserID
from app.domains.upload.storage import ALLOWED_CONTENT_TYPES, MAX_FILE_SIZE, get_storage
from app.schemas.response import Response

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

    storage = get_storage()
    url, filename = await storage.save(content, file.content_type, file.filename or "upload")
    return Response(data={"url": url, "filename": filename})
