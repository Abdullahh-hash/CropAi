import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Detect automatically if running on the cloud serverless environment
IS_VERCEL = os.getenv("VERCEL")

if IS_VERCEL:
    # Use a secure, ephemeral async in-memory space for serverless live operations
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    # Use your persistent physical database file on your local desktop machine
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