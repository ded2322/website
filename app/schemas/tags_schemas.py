from pydantic import BaseModel


class STag(BaseModel):
    name_tag: str


class SUpdateTag(BaseModel):
    old_tag_goods: str
    new_tag_goods: str
