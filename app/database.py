import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Retrieve the Turso environment keys injected by Vercel
DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if DATABASE_URL:
    # Clean up the prefix for the official driver requirement
    # Converts 'libsql://your-db.turso.io' to the format SQLAlchemy expects
    clean_url = DATABASE_URL.replace("libsql://", "")
    
    # Complete official production string connection setup
    connection_string = f"sqlite+libsql://{clean_url}/?authToken={AUTH_TOKEN}&secure=true"
    
    engine = create_engine(connection_string, connect_args={"check_same_thread": False})
else:
    # 2. Flawless fallback to local development sqlite file on your laptop
    engine = create_engine("sqlite:///./sqlite.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)