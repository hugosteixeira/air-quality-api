from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = "sqlitecloud://crhzpe9thk.g2.sqlite.cloud:8860/air_quality.db?apikey=FzWZJqldrYQxJPIYzX6rPTowcCzhE40xFthINUFNlb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
