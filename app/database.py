import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check if running live on Vercel production
IS_VERCEL = os.getenv("VERCEL") or os.getenv("TURSO_DATABASE_URL")

if IS_VERCEL:
    # Production Async Routing: Uses an isolated async in-memory instance
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    # Local Desktop Development Async Routing
    DATABASE_URL = "sqlite+aiosqlite:///./sqlite.db"

# 1. Initialize the Asynchronous Engine
engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 2. Build the Async Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    # Asynchronously spin up the metadata schema mapping tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)