import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class Transaction(Base):
    __tablename__ = "Transaction"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    recording_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.User.id"), nullable=False)
    credit_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.User.id"))
    debit_user_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.User.id"))
    other_party = Column(String)
    heading = Column(String, nullable=False)
    description = Column(String)
    transaction_mode = Column(String, nullable=False)
    shared_transaction = Column(Boolean, nullable=False)
    category = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.UserTransactionsCategory.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    currency_code = Column(ForeignKey(f"{DB_SCHEMA}.Country.id"), nullable=False)