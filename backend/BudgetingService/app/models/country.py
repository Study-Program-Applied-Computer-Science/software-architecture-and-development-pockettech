import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


class Country(Base):
    __tablename__ = "Country"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    phone_code = Column(String, nullable=False, unique=True)

    # Relationships
    budgets = relationship("Budget", back_populates="currency")
    users = relationship("User", back_populates="country")
