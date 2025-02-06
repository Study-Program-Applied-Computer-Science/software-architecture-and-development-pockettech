import os
import uuid
from fastapi import FastAPI
import uvicorn
from app.routers.transactions import router as transaction_router
from app.config import settings
from app.routers.publicKeyRoute import router as public_key_router

from app.database.init_db import init_db

from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

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

SERVICE_NAME = settings.service_name

app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])
app.include_router(public_key_router)

@app.get("/")
def read_root():
    return {"message": "Type /docs to see the API documentation."}

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8005))
#     uvicorn.run(app, host="127.0.0.1", port=port)