from sqlalchemy import select, func

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
    async def show_goods_reviews(cls, id_goods):
        async with async_session_maker() as session:
            """
            select goods.title, tags.tag, reviews.stars, "user".user_name
            from goods
            left join tags ON goods.tag_id = tags.id
            left join reviews on goods.id = reviews.id_goods 
            left join "user" on reviews.id_user = "user".id
            """
            query = (
                select(cls.model.id.label("id_goods"), cls.model.title.label("title_goods"),
                       cls.model.description.label("description_goods"),
                       Tags.tag,
                       Reviews.stars, Reviews.title.label("title_reviews"),
                       Reviews.description.label("reviews_description"),
                       User.user_name
                       )
                .select_from(cls.model)
                .join(Tags, cls.model.tag_id == Tags.id, isouter=True)
                .join(Reviews, cls.model.id == Reviews.id_goods, isouter=True)
                .join(User, Reviews.id_user == User.id, isouter=True)
                .filter(cls.model.id == id_goods)
            )
            result = await session.execute(query)
            return result.mappings().all()
