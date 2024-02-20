from app.dao.base import BaseDao
from app.models.users_models import User


class UserDao(BaseDao):
    model = User
