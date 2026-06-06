"""
Database session management

For development without async PostgreSQL drivers (asyncpg/psycopg2-binary),
this module falls back to SQLite in-memory database.
"""

import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

from app.core.config import settings


def get_database_url():
    """
    Get the appropriate database URL.
    Falls back to SQLite in-memory if PostgreSQL drivers are not available
    or if DATABASE_URL is not set.
    """
    # Check if we should use SQLite fallback
    use_sqlite = False
    
    # Check if DATABASE_URL is set to PostgreSQL
    db_url = str(settings.DATABASE_URL)
    
    # If DEBUG mode and no explicit PostgreSQL URL, use SQLite
    if settings.DEBUG and not db_url.startswith("postgresql"):
        use_sqlite = True
    
    # Try to import asyncpg to check if it's available
    try:
        import asyncpg
    except ImportError:
        # asyncpg not available, check if we're trying to use PostgreSQL
        if db_url.startswith("postgresql"):
            print("WARNING: asyncpg not installed. Falling back to SQLite for development.")
            print("To use PostgreSQL, install asyncpg: pip install asyncpg")
            use_sqlite = True
    
    if use_sqlite:
        # Use in-memory SQLite for development
        return "sqlite+aiosqlite:///:memory:"
    
    return db_url


# Create async engine
async_engine = create_async_engine(
    get_database_url(),
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
        get_database_url(),
        echo=settings.DEBUG,
    ).sync_engine
    
    SessionLocal = sessionmaker(bind=sync_engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
