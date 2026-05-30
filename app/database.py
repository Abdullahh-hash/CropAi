import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Check if we are running in production on Vercel
IS_VERCEL = os.getenv("VERCEL") or os.getenv("TURSO_DATABASE_URL")

if IS_VERCEL:
    # Production: Use an optimized, highly isolated in-memory engine 
    # This completely completely avoids Vercel's read-only file system restriction
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Local Development: Read/Write to your physical project folder file
    DATABASE_URL = "sqlite:///./sqlite.db"
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Automatically schema-map and spin up tables into memory or on disk safely
    Base.metadata.create_all(bind=engine)