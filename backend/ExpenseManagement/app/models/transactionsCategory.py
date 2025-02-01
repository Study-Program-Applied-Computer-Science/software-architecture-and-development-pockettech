import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class TransactionsCategory(Base):
    __tablename__ = "TransactionsCategory"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)
    expense = Column(Boolean, nullable=False)
