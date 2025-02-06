import uuid

from sqlalchemy import Column,Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base  
import os
from dotenv import load_dotenv

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")

class SharedGroup(Base):
    __tablename__ = "SharedGroup"
    __table_args__ = {"schema": DB_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = Column(Text, nullable=False)

