from app.models.tags_models import Tags
from app.dao.base import BaseDao


class TagsDao(BaseDao):
    model = Tags
