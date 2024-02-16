from app.models.users_models import User
from app.dao.base import BaseDao


class UserDao(BaseDao):
    model = User
