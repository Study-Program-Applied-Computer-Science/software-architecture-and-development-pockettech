from sqlalchemy import Column, Integer, Text
from app.db.database import Base

class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    extracted_text = Column(Text, nullable=False)
