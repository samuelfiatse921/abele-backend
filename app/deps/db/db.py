from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine

from app.user.models.base import Base
from app.settings import settings


# Step 1: Create engine and session maker ONCE
engine: AsyncEngine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def initialize_db(app):
    # Step 2: Store them in app state
    app.state.db_session_maker = session_maker

    # Step 3: Run DB initialization (e.g., create tables)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine


# Dependency for getting the database session
async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_maker = request.app.state.db_session_maker

    async with session_maker() as session:
        yield session

