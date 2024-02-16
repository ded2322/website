from pydantic import BaseModel


class STag(BaseModel):
    tag: int


class SUpdateTag(BaseModel):
    old_tag_goods: str
    new_tag_goods: str
