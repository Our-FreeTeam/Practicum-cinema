from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

p = settings.postgres_settings
DATABASE_URL = f"postgresql+asyncpg://{p.user}:{p.password}@{p.host}{p.port}/{p.dbname}"

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
metadata = MetaData()


async def get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
