from fastapi import FastAPI
from app.routes.ocr import router as ocr_router

# Create FastAPI instance
app = FastAPI()

# Register the OCR route
app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])


# Optional: Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to the OCR API!"}
