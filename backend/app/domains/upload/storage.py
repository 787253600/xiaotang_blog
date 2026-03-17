"""存储后端抽象层 — 支持本地存储，可扩展至 OSS/S3/COS/R2"""

import abc
import uuid
from pathlib import Path

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
UPLOAD_DIR = Path("static/uploads")


class StorageBackend(abc.ABC):
    """存储后端抽象基类"""

    @abc.abstractmethod
    async def save(self, content: bytes, content_type: str, original_filename: str) -> tuple[str, str]:
        """
        保存文件，返回 (url, filename)。
        url  — 可公开访问的 URL
        filename — 存储后的文件名
        """
        ...


class LocalStorageBackend(StorageBackend):
    """本地文件系统存储（保存到 static/uploads/）"""

    def __init__(self, upload_dir: Path = UPLOAD_DIR) -> None:
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, content: bytes, content_type: str, original_filename: str) -> tuple[str, str]:
        ext = _ext_from_content_type(content_type)
        filename = f"{uuid.uuid4().hex}{ext}"
        dest = self.upload_dir / filename
        dest.write_bytes(content)
        url = f"/static/uploads/{filename}"
        return url, filename


def _ext_from_content_type(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }
    return mapping.get(content_type, ".bin")


def get_storage() -> StorageBackend:
    """工厂函数 — 根据 STORAGE_BACKEND 配置返回对应实现。"""
    try:
        from app.config import get_settings
        settings = get_settings()
        backend = getattr(settings, "storage_backend", "local")
    except Exception:
        backend = "local"

    if backend == "local":
        return LocalStorageBackend()

    # 预留：OSS / S3 / COS / R2 实现可在此扩展
    raise NotImplementedError(f"存储后端 '{backend}' 尚未实现")
