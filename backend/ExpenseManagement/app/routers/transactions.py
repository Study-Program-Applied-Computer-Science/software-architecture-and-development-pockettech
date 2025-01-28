import uuid

from app.crud import crud
from app.schemas import transaction
from fastapi import APIRouter, Depends, HTTPException   # New imports
from sqlalchemy.orm import Session
from app.database.database import get_db


router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/", response_model=transaction.TransactionBase)
# def create_transaction(transaction: transaction.TransactionCreate, db: Session = Depends(get_db)):
#     return crud.create_transaction(db, transaction)

@router.get("/", response_model=list[transaction.TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)
    # return "Hello, World!"