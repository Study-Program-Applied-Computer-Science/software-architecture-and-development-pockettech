import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base  # Assuming Base is correctly defined in your project
from app.models.shared_group import SharedGroup  # Import SharedGroup model
from app.models.user import User  # Import User model

class SharedGroupParticipants(Base):
    __tablename__ = "SharedGroupParticipants"
    __table_args__ = {"schema": "FinancePlanner"}  # Specify the schema

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID, ForeignKey("FinancePlanner.SharedGroup.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    participant_user_id = Column(UUID, ForeignKey("FinancePlanner.User.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    # Relationships
#     group = relationship("SharedGroup", back_populates="participants", lazy="joined")
#     participant_user = relationship("User", back_populates="participated_groups", lazy="select")

# # Define back_populates in SharedGroup and User models (if not already defined)
# SharedGroup.participants = relationship("SharedGroupParticipants", back_populates="group")
# User.participated_groups = relationship("SharedGroupParticipants", back_populates="participant_user")
