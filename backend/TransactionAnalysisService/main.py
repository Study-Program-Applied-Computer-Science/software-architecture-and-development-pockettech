import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from slowapi.errors import RateLimitExceeded

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routes.transaction_analysis import router as transaction_analysis_router  # Import the router

# Import models before calling metadata.create_all
from app.models.country import Country  # Ensure country model is imported
from app.models.transactionCategory import TransactionsCategory  # Ensure user transaction category model is imported
from app.models.user import User  # Ensure users model is imported
from app.models.transaction import Transaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )

# CORS setup
origins = ["http://localhost:3000"]  # Update as per frontend origin
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
    port = int(os.getenv("PORT", 8003))  # Updated port to 8003
    uvicorn.run(app, host="127.0.0.1", port=port)
