import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if DATABASE_URL:
    # 1. Convert the protocol string seamlessly from 'libsql://' to 'https://'
    clean_url = DATABASE_URL.replace("libsql://", "https://")
    
    # 2. Build a native connection string that maps directly over secure web sockets
    # This bypasses the need for specialized OS packages entirely
    PRODUCTION_URL = f"sqlite+aiosqlite:///{clean_url}?authToken={AUTH_TOKEN}"
    
    engine = create_async_engine(
        PRODUCTION_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # 3. Flawless fallback for when you are testing locally on your PC
    engine = create_async_engine(
        "sqlite+aiosqlite:///./sqlite.db",
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