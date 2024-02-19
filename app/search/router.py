from fastapi import APIRouter

from app.dao.goods_dao import GoodsDao
router = APIRouter (
    prefix="/search",
    tags=["Search"]
)

@router.get("",status_code=200,summary="search goods")
async def search_goods(name_goods:str):
    """
    Поиск товара
    :param name_goods - название товара
    """
    result = await GoodsDao.found_search_goods(name_goods)
    if not result:
        return None
    return result