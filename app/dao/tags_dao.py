from app.dao.base import BaseDao
from app.models.tags_models import Tags


class TagsDao(BaseDao):
    model = Tags
