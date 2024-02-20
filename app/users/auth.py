from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.config import settings
from app.dao.user_dao import UserDao

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verification_password(input_password, hashed_password) -> bool:
    return pwd_context.verify(input_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY)


async def authenticate_user(username: str, password: str):
    user = await UserDao.found_one_or_none(user_name=username)
    if not user or not verification_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль"
        )

    return user
