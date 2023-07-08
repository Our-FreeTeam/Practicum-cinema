from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from sql_app.database import async_session


async def get_db(request: Request) -> AsyncSession:
    async with async_session() as session:
        request.state.db = session
        yield session
