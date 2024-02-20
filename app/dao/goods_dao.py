from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDao
from app.database import async_session_maker
from app.logger import logger
from app.models.goods_models import Goods
from app.models.reviews_models import Reviews
from app.models.tags_models import Tags


class GoodsDao(BaseDao):
    model = Goods

    @classmethod
    async def show_goods(cls, tag=None):
        """
        Отображает все товары из выбраной категории
        """
        async with async_session_maker() as session:
            try:
                """
                SELECT goods.title, goods.description,goods.image_path, tags.tag, AVG(reviews.stars) as avarage_stars
                FROM goods
                LEFT JOIN tags ON goods.tag_id = tags.id
                LEFT JOIN reviews ON goods.id = reviews.id_goods
                GROUP BY goods.title, goods.description,goods.image_path, tags.tag
                """
                query = (
                    select(
                        cls.model.title,
                        cls.model.description,
                        cls.model.image_path,
                        Tags.tag,
                        func.round(func.avg(Reviews.stars), 0).label("avarage_stars"),
                    )
                    .select_from(cls.model)
                    .join(Tags, cls.model.tag_id == Tags.id, isouter=True)
                    .join(Reviews, cls.model.id == Reviews.id_goods, isouter=True)
                    .group_by(
                        cls.model.title,
                        cls.model.description,
                        cls.model.image_path,
                        Tags.tag,
                    )
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
                    select(
                        cls.model,
                        func.round(func.avg(Reviews.stars), 0).label("avarage_stars"),
                    )
                    .join(Reviews, cls.model.id == Reviews.id_goods, isouter=True)
                    .options(selectinload(cls.model.reviews))
                    .filter(cls.model.id == id_goods)
                    .group_by(cls.model.id)
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
                SELECT goods.id,goods.title, ROUND(AVG(reviews.stars),0) AS avarage_stars
                FROM goods
                JOIN reviews ON goods.id = reviews.id_goods
                WHERE goods.title LIKE '%user_input%'
                GROUP BY goods.id
                """
                query = (
                    select(
                        cls.model.id.label("id_goods"),
                        cls.model.title.label("title_goods"),
                        cls.model.image_path,
                        func.round(func.avg(Reviews.stars), 0).label("avarage_stars"),
                    )
                    .join(Reviews, cls.model.id == Reviews.id_goods, isouter=True)
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
