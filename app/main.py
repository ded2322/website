import time
from fastapi import FastAPI, Request

from app.users.router import router_auth, router_user
from app.tags.router import router_tags, router_tag
from app.goods.router import router as goods_router
from app.reviews.router import router as reviews_router
from app.basket.router import router as basket_router
from app.logger import logger

app = FastAPI()

# todo покрыть тестами
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_tags)
app.include_router(router_tag)
#todo сделать вложенную структуру отзывов
app.include_router(goods_router)
app.include_router(reviews_router)
# todo сделать так,чтобы можно было только один товар только одного вида добавить
app.include_router(basket_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request handling time",
                extra={"process_time": round(process_time, 4)})
    return response
