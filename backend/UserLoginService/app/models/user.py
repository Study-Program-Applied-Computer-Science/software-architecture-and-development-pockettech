from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from app.db.database import Base
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

class User(Base):
    __tablename__ = "User"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    country_id = Column(ForeignKey(f"{DB_SCHEMA}.Country.id"), nullable=False)
    email_id = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
