from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

from src.core.config import app_settings

engine = create_async_engine(app_settings.DB_URL)
session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db():
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


DBSession = Annotated[AsyncSession, Depends(get_db)]
