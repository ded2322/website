from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from sqlalchemy.exc import SQLAlchemyError

from app.models.goods_models import Goods
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.models.tags_models import Tags
from app.models.reviews_models import Reviews
from app.models.users_models import User


class GoodsDao(BaseDao):
    model = Goods

    @classmethod
    async def show_goods(cls, tag=None):
        """

        :param tag:
        :return:
        """
        async with async_session_maker() as session:
            try:
                """
                SELECT goods.title, goods.description, tags.tag, reviews.review
                FROM goods
                LEFT JOIN tags ON goods.tag = tags.id
                LEFT JOIN reviews ON goods.id = reviews.goods_id
                GROUP BY goods.title, goods.description, tags.tag
                """
                query = (
                    select(cls.model.title, cls.model.description, Tags.tag,
                           func.avg(Reviews.stars).label("avarage_stars"))
                    .select_from(cls.model)
                    .join(Tags, cls.model.tag_id == Tags.id, isouter=True)
                    .join(Reviews, Reviews.id_goods == cls.model.id, isouter=True)
                    .group_by(cls.model.title, cls.model.description, Tags.tag)
                )

                if tag:
                    query = query.where(Tags.tag == tag)
                    result = await session.execute(query)
                    return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def show_info_goods(cls, id_goods: int):
        async with async_session_maker() as session:
            """
            """
            query = (
                select(cls.model).options(selectinload(cls.model.reviews))
                .filter(cls.model.id == id_goods)
            )
            res = await session.execute(query)
            return res.unique().mappings().all()
