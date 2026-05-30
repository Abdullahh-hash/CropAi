import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Look for Vercel's Turso Cloud Database string
DATABASE_URL = os.getenv("TURSO_DATABASE_URL")

if DATABASE_URL:
    # If live on Vercel, change the protocol to work with the cloud driver
    if DATABASE_URL.startswith("libsql://"):
        # Explicit setup for production cloud routing
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Fallback to your local SQLite file when developing on your PC
    DATABASE_URL = "sqlite:///./sqlite.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Keep your existing table initialization logic here...
    pass