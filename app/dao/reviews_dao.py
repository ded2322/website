from app.dao.base import BaseDao
from app.models.reviews_models import Reviews


class ReviewsDao(BaseDao):
    model = Reviews
