import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Grab the Turso variables Vercel automatically injected when you clicked "Create"
DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if DATABASE_URL:
    # Turso URLs from Vercel usually start with 'libsql://'. 
    # We change it to 'https://' so the underlying Python sqlite driver can pipe web calls
    clean_url = DATABASE_URL.replace("libsql://", "https://")
    
    # Securely append the token exactly how Python's libsql driver expects it
    PRODUCTION_URL = f"sqlite+aiosqlite:///{clean_url}?authToken={AUTH_TOKEN}"
    
    engine = create_async_engine(
        PRODUCTION_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # 2. Fallback to your local physical file when coding on your own PC
    LOCAL_URL = "sqlite+aiosqlite:///./sqlite.db"
    engine = create_async_engine(
        LOCAL_URL,
        connect_args={"check_same_thread": False}
    )

# 3. Create Session Factory
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