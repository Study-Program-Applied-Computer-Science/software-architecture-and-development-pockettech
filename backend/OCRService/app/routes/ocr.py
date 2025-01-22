from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.utils.ocr_processor import extract_text_from_image

from app.utils.ocr_processor import save_ocr_result

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/process_receipt/")
async def process_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Processes the uploaded image and stores the extracted text in the database.
    """
    # Save the uploaded file temporarily
    temp_file = f"./temp/{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # Extract text using Tesseract
    extracted_text = extract_text_from_image(temp_file)

    # Save the result to the database
    result = save_ocr_result(db, extracted_text)

    return {"id": result.id, "extracted_text": result.extracted_text}
