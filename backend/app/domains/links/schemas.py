"""友情链接数据格式"""
from pydantic import BaseModel

class LinkResponse(BaseModel):
    id:int
    name:str
    url: str
    description:str
    model_config = {"from_attributes":True}