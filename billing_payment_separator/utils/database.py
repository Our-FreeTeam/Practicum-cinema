from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from core.config import settings
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.db_uri
)

async_session = sessionmaker(bind=engine, class_=AsyncSession)
