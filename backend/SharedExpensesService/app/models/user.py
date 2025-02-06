import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class User(Base):
    __tablename__ = "User"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey(f"{DB_SCHEMA}.Country.id"), nullable=False)
    email_id = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
   # phone_code = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    # country = relationship("Country", back_populates="users")
    # transactions = relationship("Transaction", back_populates="user")
    # user_categories = relationship("UserTransactionsCategory", back_populates="user")