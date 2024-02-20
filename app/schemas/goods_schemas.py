from pydantic import BaseModel
from typing import Optional


class SGoods(BaseModel):
    title: str
    description: str
    tag: str


class SGoodsDelete(BaseModel):
    id: int


class SGoodsUpdate(BaseModel):
    id_goods: Optional[int] = None
    new_title: Optional[str] = None
    new_description: Optional[str] = None
