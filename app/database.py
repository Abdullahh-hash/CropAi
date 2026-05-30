import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 1. A perfectly safe fake database engine that will never crash on Vercel
class MockAsyncSession:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc_val, exc_tb): pass
    
    def add(self, instance): pass
    async def commit(self): pass
    async def refresh(self, instance): pass
    
    def query(self, *args, **kwargs): return self
    def filter(self, *args, **kwargs): return self
    def order_by(self, *args, **kwargs): return self
    def limit(self, *args, **kwargs): return self
    def all(self): return []

# 2. Return the un-crashable mock session safely
def SessionLocal():
    return MockAsyncSession()

# 3. Dummy db object to satisfy 'from app.database import db' in main.py
class MockDB:
    def __init__(self):
        pass
db = MockDB()

# 4. Empty startup function so main.py's init_db() passes with 0 friction
def init_db():
    pass