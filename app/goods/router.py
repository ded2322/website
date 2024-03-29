import os.path
import shutil

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from fastapi.responses import FileResponse

from app.dao.goods_dao import GoodsDao
from app.dao.tags_dao import TagsDao
from app.goods.dependencies import upload_image
from app.schemas.goods_schemas import SGoods, SGoodsDelete, SGoodsUpdate
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/goods", tags=["Goods"])


@router.get("/all", status_code=200, summary="All goods")
async def all_goods():
    """
    Отображет все доступные товары
    """
    return await GoodsDao.show_data()


@router.get("/{tag}", status_code=200, summary="Goods by tags")
async def show_tag_goods(tag: str):
    """
    Отображает все доступные товары с переданным тегом.
    """
    # проверка есть ли такой тег
    all_goods_seem_tags = await TagsDao.found_one_or_none(tag=tag)
    if not all_goods_seem_tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного тега не существует"
        )

    # Если тег существует, передается его название
    goods_tags = await GoodsDao.show_goods(all_goods_seem_tags["tag"])
    image_path = goods_tags[0]["image_path"]

    return goods_tags, FileResponse(image_path)


@router.get("/", status_code=200, summary="Goods by id")
async def show_goods(id_goods: int):
    """
    Отображает информацию, среднюю оценку, отзывы, изображение товара. Поиск по id.
    """
    info_goods = await GoodsDao.show_info_goods(id_goods)
    if not info_goods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного товара не существует"
        )

    return info_goods


async def data_goods(
    title: str = Form(), description: str = Form(), tag: str = Form()
) -> SGoods:
    """
    Для того чтобы использовать pydantic и загрузку в одном методе.
    Эта функция используется в add_goods
    """
    return SGoods(title=title, description=description, tag=tag)


@router.post("/add", status_code=200, summary="Add goods")
async def add_goods(
    data_goods: SGoods = Depends(data_goods),
    file: UploadFile = File(...),
    user_data=Depends(get_current_user),
):
    """
    Добавляет товар. Все параметры обязательны
    """
    info_tag = await TagsDao.found_one_or_none(tag=data_goods.tag)
    # Проверка,есть ли тег, в который собираются добавить товар
    if not info_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данного тега не существует"
        )

    # Проверка,есть ли товар с схожим названием
    if await GoodsDao.found_one_or_none(title=data_goods.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Товар с данным названием уже существует",
        )

    # Возращает путь до изображения /static/images/{file.filename}
    image_path = upload_image(file)

    # добавление товара в базу данных
    await GoodsDao.add_data(
        title=data_goods.title,
        description=data_goods.description,
        tag_id=info_tag["id"],
        image_path=image_path,
    )

    return {"message": "Товар успешно добавлен"}


@router.patch("/update", status_code=200, summary="Update goods")
async def update_goods(data_update: SGoodsUpdate, data_user=Depends(get_current_user)):
    """
    Обновляет данные о товаре.
    title_goods обязательный параметр. new_title и new_description Опциональные
    """
    info_goods = await GoodsDao.found_one_or_none(id=data_update.id_goods)
    # проверяет есть ли товар в базе данных
    if not info_goods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Товара не существует"
        )

    # Если хотят обновить название товара
    if data_update.new_title:
        if await GoodsDao.found_one_or_none(title=data_update.new_title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Товар с данным названием уже существует",
            )

        await GoodsDao.update_data(info_goods["id"], "title", data_update.new_title)
    # Если хотят обновить описание
    if data_update.new_description:
        await GoodsDao.update_data(
            info_goods["id"], "description", data_update.new_description
        )

    return {"message": "Данные успешно обновлены"}


@router.delete("/delete", status_code=204, summary="Delete goods")
async def delete_goods(data_goods: SGoodsDelete, user_data=Depends(get_current_user)):
    """
    Удаляет товар по названию.
    Каскадное удаление. Удаляются все отзывы к товару
    """
    info_goods = await GoodsDao.found_one_or_none(id=data_goods.id)
    # проверяет есть ли товар в базе данных
    if not info_goods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден"
        )
    await GoodsDao.delete(id=info_goods["id"])
