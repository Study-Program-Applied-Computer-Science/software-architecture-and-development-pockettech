import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class UserTransactionsCategory(Base):
    __tablename__ = "UserTransactionsCategory"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.User.id"), nullable=False)
    category = Column(String, nullable=False)
    expense = Column(Boolean, nullable=False)

    # user = relationship("User", back_populates="user_categories")
    # transactions = relationship("Transaction", back_populates="category")
    # budgets = relationship("Budget", back_populates="category")

