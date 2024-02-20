from sqladmin import Admin, ModelView

from app.models.basket_models import Basket
from app.models.goods_models import Goods
from app.models.reviews_models import Reviews
from app.models.tags_models import Tags
from app.models.users_models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.user_name]
    column_details_exclude_list = [User.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class TagsAdmin(ModelView, model=Tags):
    column_list = [Tags.id, Tags.tag, Tags.goods_tag]
    name = "Тег"
    name_plural = "Теги"
    icon = "fa-solid fa-tags"


class GoodsAdmin(ModelView, model=Goods):
    column_list = [Goods.id, Goods.title, Goods.tag]
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-cart-shopping"


class ReviewsAdmin(ModelView, model=Reviews):
    column_list = [Reviews.id, Reviews.name_user, Reviews.stars, Reviews.goods]
    name = "Отзыв"
    name_plural = "Отзывы"
    icon = "fa-solid fa-star"


class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.username, Basket.goods]
    name = "Корзина"
    name_plural = "Корзина"
    icon = "fa-solid fa-basket-shopping"
