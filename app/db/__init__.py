from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.configs import db_settings

Base = declarative_base()


engine: AsyncEngine = create_async_engine(
    db_settings.POSTGRES_URL,
    poolclass=AsyncAdaptedQueuePool,
    echo=False,
)

Session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False
)
