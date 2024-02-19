from fastapi import APIRouter

from app.dao.goods_dao import GoodsDao
router = APIRouter (
    prefix="/search"
)

@router.get("")
async def search_goods(name_goods:str):
    result = await GoodsDao.found_search_goods(name_goods)
    if not result:
        return None
    return result