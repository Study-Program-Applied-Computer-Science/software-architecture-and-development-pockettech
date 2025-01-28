from sqlalchemy import Column, Integer, String
from app.db.database import Base

class ShareType(Base):
    __tablename__ = "ShareType"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    share_type = Column(String, nullable=False, unique=True)
