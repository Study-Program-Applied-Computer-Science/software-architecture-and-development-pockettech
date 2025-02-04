import os
import sys

from app.utils.logging import setup_logger

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger = setup_logger()

try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"options": f"-csearch_path={DB_SCHEMA}"}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection successful.")
    print("Database connection successful.")
except Exception as e:
    logger.error(f"Database connection failed. {e}")
    print("Database connection failed.")
    print(e)
    sys.exit(1)


def get_db():
    db = SessionLocal()
    try:
        print(f"Session created, using DB schema: {DB_SCHEMA}")
        yield db
    finally:
        db.close()
        print(f"Session closed for DB schema: {DB_SCHEMA}")
