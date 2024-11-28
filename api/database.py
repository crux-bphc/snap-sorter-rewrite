from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234567890@localhost/snapsorter" # change to env var later
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()