"""友情链接路由"""

from fastapi import APIRouter
from sqlalchemy import select

from app.dependencies import DBSession
from app.domains.links.models import Link
from app.domains.links.schemas import  LinkResponse

router = APIRouter(prefix="/links", tags=["友情链接"])

@router.get("", response_model=list[LinkResponse])
async def get_links(session:DBSession):
    result = await session.execute(select(Link).order_by(Link.created_at.desc()))
    return result.scalars().all()