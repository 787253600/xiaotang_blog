"""标签路由 /api/v1/tags"""

from fastapi import APIRouter

from app.dependencies import CurrentUserID, DBSession
from app.domains.tags.schemas import TagCreate, TagResponse, TagUpdate
from app.domains.tags.service import TagService
from app.schemas.response import Response

router = APIRouter(prefix="/tags", tags=["标签"])


@router.get("", response_model=Response[list[TagResponse]])
async def list_tags(session: DBSession):
    service = TagService(session)
    data = await service.get_all()
    return Response(data=data)


@router.post("", response_model=Response[TagResponse], status_code=201)
async def create_tag(body: TagCreate, session: DBSession, _: CurrentUserID):
    service = TagService(session)
    data = await service.create(body)
    return Response(data=data)


@router.put("/{tag_id}", response_model=Response[TagResponse])
async def update_tag(
    tag_id: int, body: TagUpdate, session: DBSession, _: CurrentUserID
):
    service = TagService(session)
    data = await service.update(tag_id, body)
    return Response(data=data)


@router.delete("/{tag_id}", response_model=Response[None])
async def delete_tag(tag_id: int, session: DBSession, _: CurrentUserID):
    service = TagService(session)
    await service.delete(tag_id)
    return Response(message="删除成功")
