from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import app_settings

engine = create_async_engine(app_settings.DB_URL)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            # todo log
            await session.rollback()
            raise
