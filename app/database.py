import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Vercel injects the VERCEL environment variable automatically at runtime
IS_VERCEL = os.getenv("VERCEL")
TURSO_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if IS_VERCEL:
    if TURSO_URL and TURSO_TOKEN:
        # Production: Connect to your live remote Turso Cloud Database
        # Convert libsql:// to https:// so the python sqlite driver can communicate over web sockets
        clean_url = TURSO_URL.replace("libsql://", "https://")
        DATABASE_URL = f"sqlite+aiosqlite:///{clean_url}?authToken={TURSO_TOKEN}"
    else:
        # Production Fallback: Temporary, crash-safe in-memory instance if environment variables aren't set yet
        DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    # Local Development: Standard physical file on your local machine
    DATABASE_URL = "sqlite+aiosqlite:///./sqlite.db"

# Create the asynchronous engine with optimized threading arguments for SQLite
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if ":///:memory:" in DATABASE_URL or "localhost" in DATABASE_URL or "./" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    # Only try to create tables if we aren't hitting a remote production API that already has schemas
    if not TURSO_URL:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)