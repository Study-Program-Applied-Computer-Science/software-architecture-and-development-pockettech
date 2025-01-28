import os
import sys
# import logging

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")


# Debugging: Print environment variables related to DB connection
print(f"DB Schema: {os.getenv('DB_SCHEMA')}")
print(f"DB Host: {os.getenv('DB_HOST')}")
print(f"DB Port: {os.getenv('DB_PORT')}")
print(f"DB User: {os.getenv('DB_USER')}")
print(f"DB Password: {os.getenv('DB_PASSWORD')}")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"options": f"-csearch_path={DB_SCHEMA}"}
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
        print(f"Session created, using DB schema: {DB_SCHEMA}")
        yield db
    finally:
        db.close()
        print(f"Session closed for DB schema: {DB_SCHEMA}")