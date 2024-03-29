import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import (BasketAdmin, GoodsAdmin, ReviewsAdmin, TagsAdmin,
                             UserAdmin)
from app.basket.router import router as basket_router
from app.database import engine
from app.goods.router import router as goods_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.reviews.router import router as reviews_router
from app.search.router import router as search_router
from app.tags.router import router_tag, router_tags
from app.users.router import router_auth, router_user

# Создание Fastapi
app = FastAPI()
# "Показывает" место где храняться статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Создание админ.панели
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Подключение маршрутов
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_tags)
app.include_router(router_tag)
app.include_router(goods_router)
app.include_router(reviews_router)
app.include_router(basket_router)
app.include_router(search_router)
app.include_router(pages_router)

admin.add_view(UserAdmin)
admin.add_view(GoodsAdmin)
admin.add_view(TagsAdmin)
admin.add_view(ReviewsAdmin)
admin.add_view(BasketAdmin)


origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Request handling time", extra={"process_time": round(process_time, 4)}
    )
    return response
