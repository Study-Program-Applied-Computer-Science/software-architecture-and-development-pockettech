import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")

# Debugging: Log environment variables related to DB connection
logger.info(f"DB Schema: {DB_SCHEMA}")
logger.info(f"DB Host: {DB_HOST}")
logger.info(f"DB Port: {DB_PORT}")
logger.info(f"DB User: {DB_USER}")
# Do not log DB_PASSWORD for security reasons

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"options": f"-csearch_path={DB_SCHEMA}"}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    logger.info("Database connection successful.")
except Exception as e:
    logger.error("Database connection failed.", exc_info=True)
    sys.exit(1)

def get_db():
    db = SessionLocal()
    try:
        logger.info(f"Session created, using DB schema: {DB_SCHEMA}")
        yield db
    finally:
        db.close()
        logger.info(f"Session closed for DB schema: {DB_SCHEMA}")
