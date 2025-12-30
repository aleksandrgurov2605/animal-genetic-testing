import jwt
import pytest
import json
from datetime import datetime, timedelta, date

from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.db.database import Base, async_session_maker, async_engine

from app.main import app as fastapi_app, app
from app.models import AnimalGeneticTests, User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_users.json", encoding="utf8") as file:
        user_data = json.load(file)[0]

    with open("tests/mock.json", encoding="utf8") as file:
        data = json.load(file)

    async with async_session_maker() as session:
        user = User(**user_data)
        session.add(user)
        await session.flush()

        for animal in data:
            animal["test_date"] = date.fromisoformat(animal["test_date"])
            animal = AnimalGeneticTests(**animal)
            session.add(animal)

        await session.commit()


@pytest.fixture(scope="function")
def test_user_token():
    def _create_token(username: str):
        payload = {
            "sub": username,
            "exp": datetime.now() + timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return _create_token


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
