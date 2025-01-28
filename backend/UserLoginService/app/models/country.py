from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    phone_code = Column(String, unique=True, nullable=False)