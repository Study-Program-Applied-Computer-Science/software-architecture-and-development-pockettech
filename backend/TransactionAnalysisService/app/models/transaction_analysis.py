import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

# Transaction Model Definition
class Transaction(Base):
    __tablename__ = "Transaction"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    recording_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.users.id"), nullable=False)
    credit_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.users.id"))
    debit_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.users.id"))
    other_party = Column(String)
    heading = Column(String, nullable=False)
    description = Column(String)
    transaction_mode = Column(String, nullable=False)
    shared_transaction = Column(Boolean, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.UserTransactionsCategory.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    currency_code = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.country.id"), nullable=False)

