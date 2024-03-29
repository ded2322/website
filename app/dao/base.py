from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.logger import logger


class BaseDao:
    model = None

    @classmethod
    async def show_data(cls):
        """
        Отображает все данные в таблице
        """
        async with async_session_maker() as session:
            try:
                query = select(cls.model)
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Database exc show database: {str(e)}"
                else:
                    msg = f"Unknown exc: {str(e)}"

                logger.error(msg, exc_info=True)

    @classmethod
    async def add_data(cls, **kwargs):
        """
        Добавляет новые данные в таблицу
        """
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc insert into database: {str(e)}"
                else:
                    msg = f"Unknown exc insert into database: {str(e)}"
                logger.error(msg, exc_info=True)

    @classmethod
    async def found_one_or_none(cls, **kwargs):
        """
        В таблице ищет данные,по заданным параметрам из **kwargs
        """
        async with async_session_maker() as session:
            try:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
                return result.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc found_one_or_none database: {str(e)}"
                else:
                    msg = f"Unknown exc found_one_or_none database: {str(e)}"
                logger.error(msg)

    @classmethod
    async def delete(cls, **kwargs):
        """
        Удаляет данные из таблицы
        """
        async with async_session_maker() as session:
            try:
                query = delete(cls.model).filter_by(**kwargs)
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc delete data: {str(e)}"
                else:
                    msg = f"Unknown exc delete data: {str(e)}"
                logger.error(msg, exc_info=True)

    @classmethod
    async def update_data(cls, id_column: int, column, new_data):
        """
        Обновляет данные в таблице
        :param id_column - id строки которую нужно изменить
        :param column - колонка которую нужно изменить
        :param new_data - новые данные для изменения
        """
        async with async_session_maker() as session:
            try:
                # SELECT * FROM model WHERE id = id_column;
                query = await session.get(cls.model, id_column)
                # Проверяет есть ли в таблице атрибут column
                # if model.column
                if hasattr(query, column):
                    # model.column = new_data
                    setattr(query, column, new_data)
                    await session.commit()
                    return None
                else:
                    raise ValueError("Неправильные данные")
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    msg = f"Exc update data: {str(e)}"
                else:
                    msg = f"Unknown exc update data: {str(e)}"
                logger.error(msg)
