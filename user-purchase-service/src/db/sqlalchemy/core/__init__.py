from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.core.config import get_settings_instance

engine = create_async_engine(
        get_settings_instance().POSTGRES_DSN,
        echo=True,
        future=True,
    )

Base = declarative_base()


async def init_models():
    from src.db.sqlalchemy import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
