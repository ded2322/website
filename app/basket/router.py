from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.basket_schemas import SBasket
from app.users.dependencies import get_current_user
from app.dao.basket_dao import BasketDao
from app.dao.goods_dao import GoodsDao

router = APIRouter(
    prefix="/basket",
    tags=["Basket"]

)


@router.get("/all", status_code=200, summary="All baskets")
async def show_basket():
    """
    Отдает все корзины и их содержимое
    """
    return await BasketDao.show_data()


@router.get("/user")
async def show_basket_user(data_user=Depends(get_current_user)):
    return await BasketDao.show_basket_user(data_user["id"])


@router.post("/add", status_code=200, summary="Add goods in basket")
async def add_goods_basket(data_basket: SBasket, data_user=Depends(get_current_user)):
    if not await GoodsDao.found_one_or_none(id=data_basket.id_goods):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")

    await BasketDao.add_data(id_goods=data_basket.id_goods, id_user=data_user["id"])

    return {"message": "Товар успешно доваблен в корзину"}


@router.delete("/delete",status_code=204,summary="Delete goods for basket")
async def delete_basket(data_basket: SBasket, data_user=Depends(get_current_user)):
    info_basket = await BasketDao.found_basket(id_goods=data_basket.id_goods)
    if not info_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не найден")
    await BasketDao.delete(id_goods=data_basket.id_goods, id_user=data_user["id"])

