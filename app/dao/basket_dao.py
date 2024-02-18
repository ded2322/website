from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.dao.base import BaseDao
from app.models.basket_models import Basket
from app.models.users_models import User
from app.models.goods_models import Goods


class BasketDao(BaseDao):
    model = Basket

    @classmethod
    async def show_basket_user(cls, user_id: int):
        async with async_session_maker() as session:
            try:
                query = (
                    select(Goods.title, User.user_name.label("username"))
                    .select_from(cls.model)
                    .join(Goods, Goods.id == Basket.id_goods)
                    .join(User, Basket.id_user == User.id)
                    .filter(cls.model.id_user == user_id)
                )
                result = await session.execute(query)
                return result.mappings().all()

            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def delete(cls, id_user, id_goods):
        async with async_session_maker() as session:
            try:
                """
                DELETE FROM basket
                WHERE basket.id_goods = 10 and basket.id_user=40
                """
                query = (
                    delete(cls.model).filter(cls.model.id_goods == id_goods, cls.model.id_user == id_user)
                )
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def found_basket(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                """
                DELETE FROM basket
                WHERE basket.id_goods = 10 and basket.id_user=40
                """
                query = (
                    select(cls.model).filter_by(**kwargs)
                )
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")
