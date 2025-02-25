from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
import uvicorn
from common.config.logging import setup_logger
from common.config.correlation import CorrelationIdMiddleware

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routes.budget import router as budget_router
from app.routes.publicKeyRoute import router as public_key_router
from app.db.init_db import init_db


Base.metadata.create_all(bind=engine)

init_db()

app = FastAPI()


# CORS setup
origins = ["http://localhost:5173"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
SERVICE_NAME = os.getenv("SERVICE_NAME")

logger = setup_logger(SERVICE_NAME)

# Add Correlation ID Middleware
app.add_middleware(CorrelationIdMiddleware)

# Add the exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )

# Include routers
app.include_router(budget_router, prefix="/budget", tags=["budget"])
app.include_router(public_key_router)

@app.get("/")
def read_root():
    logger.info("Root endpoint hit.")
    return {"message": "Welcome to the Budgeting Service"}

@app.get("/{budget_id}")
def read_budget(budget_id: uuid.UUID):
    logger.info(f"Fetching details for budget ID: {budget_id}")
    return {"budget_id": budget_id, "details": "Budget details would be here"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)
