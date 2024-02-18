import pytest
import json
import asyncio

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.config import settings
from app.models.users_models import User
from app.models.goods_models import Goods
from app.models.basket_models import Basket
from app.models.reviews_models import Reviews
from app.models.tags_models import Tags
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)

    def open_mock_json(name_json: str):
        with open(f"app/tests/mock_{name_json}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    user = open_mock_json("user")
    tags = open_mock_json("tags")
    goods = open_mock_json("goods")
    reviews = open_mock_json("reviews")
    basket = open_mock_json("basket")

    async with async_session_maker() as session:
        add_user = insert(User).values(user)
        add_tags = insert(Tags).values(tags)
        add_goods = insert(Goods).values(goods)
        add_reviews = insert(Reviews).values(reviews)
        add_basket = insert(Basket).values(basket)

        await session.execute(add_user)
        await session.execute(add_tags)
        await session.execute(add_goods)
        await session.execute(add_reviews)
        await session.execute(add_basket)

        await session.commit()


# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
