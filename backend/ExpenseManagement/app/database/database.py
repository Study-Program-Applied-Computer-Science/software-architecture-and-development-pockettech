from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys

load_dotenv()

DATABASE_USER = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_HOST = os.getenv("DB_HOST")
DATABASE_PORT = os.getenv("DB_PORT")
DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_SCHEMA = os.getenv("DB_SCHEMA")

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"options": f"-csearch_path={DATABASE_SCHEMA}"}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    print("Database connection successful.")
except Exception as e:
    print("Database connection failed.")
    print(e)
    sys.exit(1)


def get_db():
    db = SessionLocal()
    try:
        print(f"Session created, using DB schema: {DATABASE_SCHEMA}")
        yield db
    finally:
        db.close()
        print(f"Session closed for DB schema: {DATABASE_SCHEMA}")
