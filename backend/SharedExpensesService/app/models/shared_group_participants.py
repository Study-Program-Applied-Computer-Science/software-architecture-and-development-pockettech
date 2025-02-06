import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base  # Assuming Base is correctly defined in your project
import os
from dotenv import load_dotenv

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

class SharedGroupParticipants(Base):
    __tablename__ = "SharedGroupParticipants"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID, ForeignKey("FinancePlanner.SharedGroup.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    participant_user_id = Column(UUID, ForeignKey("FinancePlanner.User.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
