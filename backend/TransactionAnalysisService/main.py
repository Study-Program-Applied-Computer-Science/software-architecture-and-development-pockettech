import os
import uuid
from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.routes.transaction_analysis import router as transaction_analysis_router  # Import the router

Base.metadata.create_all(bind=engine)

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

# Include routers
app.include_router(transaction_analysis_router, prefix="/transaction-analysis", tags=["transaction-analysis"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8003))  # Updated port to 8003
    uvicorn.run(app, host="127.0.0.1", port=port)
