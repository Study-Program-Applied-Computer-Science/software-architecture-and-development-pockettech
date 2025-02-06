import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routes.transaction_analysis import router as transaction_analysis_router

# Import models before calling metadata.create_all
from app.models.country import Country  
from app.models.transactionCategory import TransactionsCategory 
from app.models.user import User  
from app.models.transaction import Transaction

# Import logging setup
from logging_config import logger  

# Load environment variables
load_dotenv()
SERVICE_NAME = os.getenv("SERVICE_NAME", "transaction_analysis_service")

# Initialize logger
logger.info("Logger initialized for service: %s", SERVICE_NAME)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for request: {request.url.path}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )

# CORS setup
# Update as per frontend origin
origins = ["http://localhost:3000"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transaction_analysis_router, prefix="/transaction-analysis", tags=["transaction-analysis"])


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8006))  # Updated port to 8006
    logger.info(f"Starting FastAPI service on port {port}")
    uvicorn.run(app, host="127.0.0.1", port=port)
