import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    TEST_PG_DB: str
    TEST_PG_PASSWORD: str
    TEST_PG_USER: str
    TEST_PG_HOST: str
    TEST_PG_PORT: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        extra="ignore",
    )

    @property
    def ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TEST_ASYNC_DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.TEST_PG_USER}:{self.TEST_PG_PASSWORD}"
            f"@{self.TEST_PG_HOST}:{self.TEST_PG_PORT}/{self.TEST_PG_DB}"
        )


settings = Settings()
