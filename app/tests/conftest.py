import json
from datetime import datetime

import pytest_asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.item.models import TodoItem
from app.main import app as fastapi_app
from app.utils.helpers import redis_helper


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    items = open_mock_json("items")

    for item in items:
        item["created_at"] = datetime.strptime(
            item["created_at"], "%Y-%m-%d %H:%M:%S.%f"
        )

    async with async_session_maker() as session:

        add_transactions = insert(TodoItem).values(items)

        await session.execute(add_transactions)

        await session.commit()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_redis():
    redis = await redis_helper.connect()
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@pytest_asyncio.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(fastapi_app), base_url="http://test"
    ) as ac:
        yield ac
