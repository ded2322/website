from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.goods.router import show_tag_goods

router = APIRouter(prefix="/pages", tags=["Фронтенд"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/show-image")
async def show_image(request: Request, data_goods=Depends(show_tag_goods)):
    """
    Метод для проверки работоспособности отображения изображений
    """
    items = data_goods[0]
    print(items)
    return templates.TemplateResponse("main.html", {"request": request, "items": items})
