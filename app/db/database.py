from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Строка подключения для PostgreSQl
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_ASYNC_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.ASYNC_DATABASE_URL
    DATABASE_PARAMS = {}

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=False, **DATABASE_PARAMS)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
