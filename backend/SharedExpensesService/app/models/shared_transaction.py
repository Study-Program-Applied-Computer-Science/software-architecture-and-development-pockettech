import uuid

from sqlalchemy import Column, ForeignKey, UUID, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.payment_status import PaymentStatus
from app.models.transaction import Transaction
import os
from dotenv import load_dotenv

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

class SharedTransaction(Base):
    __tablename__ = "SharedTransaction"
    __table_args__ = {"schema": DB_SCHEMA}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    
    transaction_id = Column(UUID, ForeignKey("Transaction.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    group_user_id_main = Column(UUID, ForeignKey("User.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    group_user_id_sub = Column(UUID, ForeignKey("User.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    repayment_transaction_id = Column(UUID(as_uuid=True), ForeignKey("FinancePlanner.Transaction.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    share_value = Column(Numeric, nullable=False)
    payment_status = Column(Integer, ForeignKey("PaymentStatus.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    
 