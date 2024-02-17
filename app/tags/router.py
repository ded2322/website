from fastapi import APIRouter, HTTPException, Depends, status

from app.dao.tags_dao import TagsDao
from app.schemas.tags_schemas import STag, SUpdateTag
from app.users.dependencies import get_current_user

router_tags = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)
router_tag = APIRouter(
    prefix="/tag",
    tags=["Tag"]
)


@router_tags.get("/all", status_code=200, summary="Show all tag")
async def tags():
    """
    Показывает все теги
    """
    return await TagsDao.show_data()


@router_tag.post("/add", status_code=200, summary="Add tag")
async def add_tag(data_tag: STag, user_data=Depends(get_current_user)):
    """
    Добавляет тег, только аутентифицированным пользователям
    """
    if await TagsDao.found_one_or_none(tag=data_tag.tag_goods):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данный тег уже существует")

    await TagsDao.add_data(tag=data_tag.tag_goods)
    return {"message": "Тег успешно добавлен"}


@router_tag.patch("/update", status_code=200, summary="Update tag")
async def update(data_type: SUpdateTag, user_data=Depends(get_current_user)):
    """
    Обновляет название тега, только аутентифицированным пользователям
    """
    id_tag = await TagsDao.found_one_or_none(tag=data_type.old_tag_goods)
    if not id_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данного тега не существует")

    await TagsDao.update_data(id_tag["id"], "tag", data_type.new_tag_goods)
    return {"message": "Тег успешно обновлен"}


@router_tag.delete("/delete", status_code=204, summary="Delete tag")
async def delete_tags(data_type: STag, user_data=Depends(get_current_user)):
    """
    Удаляет заданный тег, только аутентифицированным пользователям
    """
    id_tag = await TagsDao.found_one_or_none(id=data_type.tag)
    if not id_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данного тега не существует")

    await TagsDao.delete(id=id_tag["id"])
