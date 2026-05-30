import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check if running live on Vercel production
IS_VERCEL = os.getenv("VERCEL")

if IS_VERCEL:
    # Production: Stable, un-crashable async in-memory SQLite
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    # Local Desktop: Standard physical database file
    DATABASE_URL = "sqlite+aiosqlite:///./sqlite.db"

engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)