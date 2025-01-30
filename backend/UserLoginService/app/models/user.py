from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    email_id = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_code = Column(String, ForeignKey("country.phone_code"), nullable=False)
    phone_number = Column(String, nullable=False)
