import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class Budget(Base):
    __tablename__ = "Budget"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey(f"{DB_SCHEMA}.UserTransactionsCategory.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    currency_id = Column(ForeignKey(f"{DB_SCHEMA}.Country.id"), nullable=False)

