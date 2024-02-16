from fastapi import FastAPI

from app.users.router import router_auth,router_user
from app.tags.router import router_tags,router_tag
from app.goods.router import router as goods_router
from app.reviews.router import router as reviews_router
from app.basket.router import router as basket_router


app = FastAPI()
# todo ПОКРЫТЬ ТЕСТАМИ
# todo покрыть тестами и задокументировать
app.include_router(router_auth)
app.include_router(router_user)
#todo сделать проверку прав пользователя, чтобы добавлять теги, товары
#todo сделать пользователя который может удалять людей и т.д
app.include_router(router_tags)
app.include_router(router_tag)
#todo задокументрировать
app.include_router(goods_router)
app.include_router(reviews_router)
#todo сделать так,чтобы можно было только один товар только одного вида добавить
app.include_router(basket_router)
