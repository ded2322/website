from fastapi import APIRouter, Depends, HTTPException, status

from app.dao.reviews_dao import ReviewsDao
from app.schemas.reviews_schemas import SReviews, SReviewsDelete, SReviewUpdate
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/all", status_code=200, summary="Show all reviews")
async def show_reviews():
    """
    Просмотр всех доступных отзывов
    """
    return await ReviewsDao.show_data()


@router.post("/add", status_code=200, summary="Add reviews")
async def add_reviews(data_reviews: SReviews, user_data=Depends(get_current_user)):
    """
    Добавляет отзыв к товару.
    """
    # Проверка на наличие товара
    if not data_reviews.id_goods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного товара не существует"
        )
    # Проверка звезд пользователя, если меньшe 0 и больше 5 ошибка
    if data_reviews.stars < 0 or data_reviews.stars > 5:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Неправильная оценка"
        )

    # Добавление отзыва к товару
    await ReviewsDao.add_data(
        title=data_reviews.title,
        description=data_reviews.description,
        stars=data_reviews.stars,
        id_goods=data_reviews.id_goods,
        name_user=user_data["user_name"],
    )
    return {"message": "Данные успешно добавлены"}


@router.patch("/update", status_code=200, summary="Update reviews")
async def update_reviews(
    data_update: SReviewUpdate, user_data=Depends(get_current_user)
):
    """
    Обновляет данные о пользователе.
    id_reviews - обязательный параметр.
    new_title,new_description - опциональный параметр
    """
    # инфорамция по отзыву
    info_reviews = await ReviewsDao.found_one_or_none(id=data_update.id_reviews)
    # Если отзыва не существует
    if not info_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного отзыва не существует"
        )
    # Провека, что пользователь тот за того кого выдает
    if not info_reviews["id_user"] == user_data["id"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Войдите под другим пользователем",
        )

    if data_update.new_title:
        await ReviewsDao.update_data(
            data_update.id_reviews, "title", data_update.new_title
        )
    if data_update.new_description:
        await ReviewsDao.update_data(
            data_update.id_reviews, "description", data_update.new_description
        )

    return {"message": "Данные успешно обновлены"}


@router.delete("/delete", status_code=204, summary="Delete reviews")
async def delete_reviews(
    data_reviews: SReviewsDelete, data_user=Depends(get_current_user)
):
    """
    Удаляет указанный отзыв, только тот который человек уже добавил
    """
    info_reviews = await ReviewsDao.found_one_or_none(id=data_reviews.id_reviews)
    if not info_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного отзыва не существует"
        )

    if not info_reviews["name_user"] == data_user["user_name"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Войдите под другим пользователем",
        )

    await ReviewsDao.delete(id=data_reviews.id_reviews)
