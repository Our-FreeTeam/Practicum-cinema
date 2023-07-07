from abc import ABC, abstractmethod
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


class Database(ABC):
    def __init__(self):
        self.async_sessionmaker: sessionmaker | None = None

    async def __call__(self) -> AsyncIterator[AsyncSession]:
        """For use with FastAPI Depends"""
        if not self.async_sessionmaker:
            raise ValueError("async_sessionmaker not available. Run setup() first.")
        async with self.async_sessionmaker() as session:
            yield session

    @abstractmethod
    def setup(self) -> None:
        ...


# database/postgres.py
def get_connection_string(driver: str = "asyncpg") -> str:
    return f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@" \
           f"{settings.db_host}:{settings.db_port}/{settings.db_name}"


class PostgresDatabase(Database):
    def setup(self) -> None:
        async_engine = create_async_engine(
            get_connection_string(),
        )
        self.async_sessionmaker = sessionmaker(async_engine, class_=AsyncSession)


db = PostgresDatabase()
