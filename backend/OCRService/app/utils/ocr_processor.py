from PIL import Image
import pytesseract
import pytesseract

# Add this line to configure the Tesseract path explicitly
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configure Tesseract path if needed (for Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from the given image using Tesseract OCR.
    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error processing image: {e}")
from sqlalchemy.orm import Session
from app.models.models import OCRResult

def save_ocr_result(db: Session, extracted_text: str):
    """
    Saves the extracted text into the database.
    """
    ocr_result = OCRResult(extracted_text=extracted_text)
    db.add(ocr_result)
    db.commit()
    db.refresh(ocr_result)
    return ocr_result
