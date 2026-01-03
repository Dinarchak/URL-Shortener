from fastapi import Depends
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncAttrs
)
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime
from settings import config

DB_URL = f"postgresql+asyncpg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.db_name}"

engine = create_async_engine(DB_URL, pool_size=20, max_overflow=30)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)