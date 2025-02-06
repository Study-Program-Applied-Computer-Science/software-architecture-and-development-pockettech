from fastapi import FastAPI, Request
from app.db.database import engine, Base
from app.routes import (
    shared_group,
    shared_transaction
)
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from common.config.correlation import CorrelationIdMiddleware
from common.config.logging import setup_logger
from dotenv import load_dotenv
import os

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME")
logger = setup_logger(SERVICE_NAME)
# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CorrelationIdMiddleware)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )

@app.on_event("startup")
async def list_routes():
    for route in app.routes:
        print(f"Path: {route.path} | Name: {route.name}")


# CORS setup
origins = ["http://localhost:5173"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Include routers
app.include_router(shared_group.router, prefix="/shared-group", tags=["SharedGroup"])
app.include_router(shared_transaction.router, prefix="/shared-transaction", tags=["SharedTransaction"])
# app.include_router(user.router, prefix="/users",tags=["User"])

