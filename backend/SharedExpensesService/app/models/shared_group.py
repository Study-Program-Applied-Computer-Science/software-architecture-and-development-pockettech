import uuid

from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base  # Assuming Base is correctly defined in your project
from app.models.user import User  # Import User model from the same microservice

class SharedGroup(Base):
    __tablename__ = "SharedGroup"
    __table_args__ = {"schema": "FinancePlanner"}  # Specify the schema

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_user_id = Column(UUID, ForeignKey("FinancePlanner.User.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    group_name = Column(Text, nullable=False)

#     # Relationships
#     admin_user = relationship("User", back_populates="admin_groups", lazy="select")  # Link to User model
#     participants = relationship("SharedGroupParticipants", back_populates="group", lazy="select")

# # Define back_populates in the User model (if not already defined)
# User.admin_groups = relationship("SharedGroup", back_populates="admin_user")
