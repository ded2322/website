from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker


class  BaseDao:
    model = None

    @classmethod
    async def show_data(cls):
        async with async_session_maker() as session:
            try:
                query = select(cls.model)
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def insert_data(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def found_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
                return result.mappings().one_or_none()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def delete(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                query = delete(cls.model).filter_by(**kwargs)
                await session.execute(query)
                await session.commit()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")

    @classmethod
    async def update_data(cls, id_column, column, new_data):
        async with async_session_maker() as session:
            try:
                query = await session.get(cls.model, id_column)
                # понять как это работает
                if hasattr(query, column):
                    setattr(query, column, new_data)
                    await session.commit()
                else:
                    raise "Неправльный не мир, неправильные блять данные"
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    print(f"Database error: {str(e)}")
                else:
                    print(f"Unexpected error: {str(e)}")
