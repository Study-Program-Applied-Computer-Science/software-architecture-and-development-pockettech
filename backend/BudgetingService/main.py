import os
from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"message": "Welcome to Finance Management API"}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Budgeting Service"}

@app.get("/budget/{budget_id}")
def read_budget(budget_id: int):
    return {"budget_id": budget_id, "details": "Budget details would be here"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="127.0.0.1", port=port)