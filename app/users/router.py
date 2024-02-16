from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import RedirectResponse

from app.schemas.users_schemas import SUserAuth, SUserLogin, SUserUpdateData
from app.users.auth import get_password_hash, verification_password, create_access_token
from app.users.dependencies import get_current_user
from app.dao.user_dao import UserDao

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
router_user = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router_auth.post("/register", status_code=200, summary="Register user")
async def register_user(data_user: SUserAuth):
    """
    Регистрирует пользователя, а так-же создает куки.
    Обязательные параметры:
    username,
    password
    Опциональные:
    email
    """
    # Если в бд есть введенное пользователем имя или почта, выдает ошибку
    if await UserDao.found_one_or_none(user_name=data_user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Это имя уже используется")

    # Добавляет данных в бд
    await UserDao.insert_data(user_name=data_user.username, email=data_user.email,
                              hashed_password=get_password_hash(data_user.password), is_superuser=False)

    return RedirectResponse("/auth/login")


@router_auth.post("/login", status_code=200,summary="Login user")
async def login_user(response: Response, data_user: SUserLogin):
    """
    Производит аутентификацию пользователя.
    Создает куки с информацией о пользователе.
    """
    user = await UserDao.found_one_or_none(user_name=data_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя не существует")

    correct_password = verification_password(data_user.password, user.hashed_password)

    if not user or not correct_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль")
    try:
        response.set_cookie("access_token", create_access_token({"sub": str(user.id)}), httponly=True)
    except Exception as e:
        raise f"{str(e)}"

    return {"message": "Вы успешно вошли"}


@router_user.get("/me", status_code=200, summary="Info about user")
async def info_user(user_data=Depends(get_current_user)):
    """
    Показывает информацию о пользователе
    """
    return user_data


@router_user.get("/logout", status_code=204,summary="Logout user")
async def logout_user(response: Response):
    """
    Производит деаутентификация.
    Удаляет куки
    """
    try:
        response.delete_cookie("access_token")
    except Exception as e:
        raise f"{str(e)}"


@router_user.patch("/update", status_code=200, summary="Update user data")
async def update_data(new_data: SUserUpdateData, data_user=Depends(get_current_user)):
    """
    Обновляет данные пользователя.
    Имя, почту, пароль. Все опционально
    """

    if new_data.user:
        # Если такое имя уже есть, ошибка
        if await UserDao.found_one_or_none(user_name=new_data.user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данное имя уже используется")

        await UserDao.update_data(data_user["id"], "user_name", new_data.user)

    if new_data.email:
        if await UserDao.found_one_or_none(email=new_data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данная почта уже используется")

        await UserDao.update_data(data_user["id"], "email", new_data.email)

    if new_data.password:
        user_password = get_password_hash(new_data.password)
        await UserDao.update_data(data_user["id"], "hashed_password", user_password)
    return {"message" : "Данные успешно обновлены"}


@router_user.delete("/delete", status_code=204, summary="Delete user")
async def delete_user(data_user=Depends(get_current_user)):
    """
    Удаляет пользователя из базы данных
    """
    await UserDao.delete(id=data_user["id"])
