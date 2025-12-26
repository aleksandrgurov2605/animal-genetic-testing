from typing import AsyncGenerator

import pytest
import json
from datetime import date

from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.db.database import Base, async_session_maker, async_engine
from app.db.db_depends import get_async_db
from app.main import app as fastapi_app, app
from app.models import AnimalGeneticTests


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock.json", encoding="utf8") as file:
        data = json.load(file)

    async with async_session_maker() as session:
        for animal in data:
            animal["test_date"] = date.fromisoformat(animal["test_date"])
            # Create and add object
            animal = AnimalGeneticTests(**animal)
            session.add(animal)

        await session.commit()


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
