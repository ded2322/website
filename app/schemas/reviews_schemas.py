from typing import Optional

from pydantic import BaseModel, validator


class SReviews(BaseModel):
    id_goods: int
    title: str
    description: Optional[str] = None
    stars: int = 1


class SReviewUpdate(BaseModel):
    id_reviews: int
    new_title: Optional[str] = None
    new_description: Optional[str] = None


class SReviewsDelete(BaseModel):
    id_reviews: int
