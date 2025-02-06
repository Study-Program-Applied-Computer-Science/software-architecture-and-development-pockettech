import os
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")  # Default to 'public' schema

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Create the database engine
    engine = create_engine(
        DATABASE_URL,
        connect_args={"options": f"-csearch_path={DB_SCHEMA}"},  # Set schema search path
        pool_pre_ping=True,  # Enables pool pre-ping to detect stale connections
    )
    
    # Initialize session and base
    metadata = MetaData(schema=DB_SCHEMA)  # Use the schema in metadata
    Base = declarative_base(metadata=metadata)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test the connection
    with engine.connect() as connection:
        print(f"Database connection successful! Using schema: {DB_SCHEMA}")
except SQLAlchemyError as e:
    print("Error: Could not connect to the database.")
    print(f"Details: {e}")
    sys.exit(1)  # Exit if the connection fails

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
