import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Grab Turso environment variables from Vercel
DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if DATABASE_URL:
    # 1. Clean up the URL scheme for the streaming driver
    # If it starts with libsql://, convert it to a secure https:// or http:// mapping for web calls
    if DATABASE_URL.startswith("libsql://"):
        db_endpoint = DATABASE_URL.replace("libsql://", "https://")
    else:
        db_endpoint = DATABASE_URL

    # 2. Use the dedicated, stable turso client dialect string
    # This instructs SQLAlchemy exactly how to pass the authorization tokens seamlessly
    connection_string = f"sqlite+turso://{db_endpoint.replace('https://', '')}"
    
    engine = create_engine(
        connection_string, 
        connect_args={"auth_token": AUTH_TOKEN},
        echo=False
    )
else:
    # 3. Flawless fallback to local development file when working on your PC
    engine = create_engine(
        "sqlite:///./sqlite.db", 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Keep your existing table model initialization completely intact
    Base.metadata.create_all(bind=engine)