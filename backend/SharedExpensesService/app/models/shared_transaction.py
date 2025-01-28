import uuid

from sqlalchemy import Column, ForeignKey, UUID, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.share_type import ShareType
from app.models.payment_status import PaymentStatus
from app.models.transaction import Transaction

class SharedTransaction(Base):
    __tablename__ = "SharedTransaction"
    __table_args__ = {"schema": "FinancePlanner"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    
    transaction_id = Column(UUID, ForeignKey("Transaction.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    
    group_user_id_main = Column(UUID, ForeignKey("SharedGroupParticipants.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    group_user_id_sub = Column(UUID, ForeignKey("SharedGroupParticipants.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    
    # ForeignKey to ShareType and PaymentStatus (can be in this microservice or another)
    share_type_id = Column(Integer, ForeignKey("ShareType.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    share_value = Column(Numeric, nullable=False)
    payment_status = Column(Integer, ForeignKey("PaymentStatus.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    
    # Relationships
    share_type = relationship("ShareType")
    payment_status_rel = relationship("PaymentStatus")
    
    # Relationships to SharedGroupParticipants for main and sub group users
    main_group_user = relationship("SharedGroupParticipants", foreign_keys=[group_user_id_main])
    sub_group_user = relationship("SharedGroupParticipants", foreign_keys=[group_user_id_sub])

# Optional: Define back_populates if needed in this microservice
# Transaction.shared_transactions = relationship("SharedTransaction", back_populates="transaction")
