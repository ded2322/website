from jose import ExpiredSignatureError, JWTError, jwt
from fastapi import Depends, Request, HTTPException, status

from app.config import settings
from app.dao.user_dao import UserDao


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Куки не найдены"
        )
    return token


async def get_current_user(token=Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Куки истек"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат куки"
        )

    user_data = await UserDao.found_one_or_none(id=int(payload["sub"]))

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user_data
