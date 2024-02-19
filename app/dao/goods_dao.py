from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from sqlalchemy.exc import SQLAlchemyError

from app.models.goods_models import Goods
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.models.tags_models import Tags
from app.models.reviews_models import Reviews
from app.models.users_models import User
from app.logger import logger


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
                    msg = f"Exc show_goods database: {str(e)}"
                else:
                    msg = f"Unknown exc show_goods database: {str(e)}"
                logger.error(msg)

    @classmethod
    async def show_info_goods(cls, id_goods: int):
        """
        Отображает отдельно взятый товар,
        инф.по о нем, среднея оценка отзывов, отзывы
        """
        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model,
                           func.avg(Reviews.stars).label("avarage_stars"))
                    .join(Reviews, cls.model.id == Reviews.id_goods)
                    .options(selectinload(cls.model.reviews))
                    .group_by(cls.model.id)
                    .filter(cls.model.id == id_goods)
                )
                res = await session.execute(query)
                return res.unique().mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc show_info_goods database: {str(e)}"
                else:
                    msg = f"Unknown exc show_info_goods database: {str(e)}"
                logger.error(msg)

    @classmethod
    async def found_search_goods(cls, user_input: str):
        """
        Производит поиск товара по переданным значениям пользователя
        """
        async with async_session_maker() as session:
            try:
                """
                SELECT goods.id,goods.title, AVG(reviews.stars) AS avarage_stars
                FROM goods
                JOIN reviews ON goods.id = reviews.id_goods
                WHERE goods.title LIKE '%user_input%'
                GROUP BY goods.id
                """
                query = (
                    select(cls.model.id.label("id_goods"), cls.model.title.label("title_goods"),
                           func.round(func.avg(Reviews.stars), 0).label("avarage_stars")
                           )
                    .join(Reviews, cls.model.id == Reviews.id_goods)
                    .where(cls.model.title.like(f"%{user_input}%"))
                    .group_by(cls.model.id)
                )
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc found_search_goods database: {str(e)}"
                else:
                    msg = f"Unknown exc found_search_goods database: {str(e)}"
                logger.error(msg)
