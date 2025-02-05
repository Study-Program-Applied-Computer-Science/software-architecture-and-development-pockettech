import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String

from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class Country(Base):
    __tablename__ = "Country"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    phone_code = Column(String, nullable=False, unique=True)
