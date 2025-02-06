from sqlalchemy import Column, Integer, String
from app.db.database import Base


class PaymentStatus(Base):
    __tablename__ = "PaymentStatus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String, nullable=False, unique=True)
