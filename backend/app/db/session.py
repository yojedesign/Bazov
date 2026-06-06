"""
Database session management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from typing import AsyncGenerator, Optional

from app.core.config import settings

# Create async engine
async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create sync engine (for migrations)
sync_engine = None
if not settings.DEBUG:
    sync_engine = sessionmaker(bind=async_engine.sync_engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables
    """
    from app.db.base import Base
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections
    """
    await async_engine.dispose()


# For migrations
async def get_sync_db():
    """
    Get synchronous database session for migrations
    """
    from sqlalchemy.orm import Session
    
    sync_engine = create_async_engine(
        str(settings.DATABASE_URL),
        echo=settings.DEBUG,
    ).sync_engine
    
    SessionLocal = sessionmaker(bind=sync_engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
