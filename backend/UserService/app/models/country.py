from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

class Country(Base):
    __tablename__ = "Country"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    phone_code = Column(String, unique=True, nullable=False)