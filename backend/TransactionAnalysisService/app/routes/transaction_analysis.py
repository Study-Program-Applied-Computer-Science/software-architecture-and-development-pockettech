from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # Assuming get_db is defined in app.db.database to get the DB session
from app.crud.transaction_analysis import get_last_10_transactions  # Importing the function from CRUD file
from app.schemas.transaction_analysis import TransactionResponse  # Import your Pydantic response schema
from typing import List

router = APIRouter()

# API endpoint to get last 10 transactions
@router.get("/transactions/last-10", response_model=List[TransactionResponse])  # Specify response model here
def get_last_10_transactions_endpoint(db: Session = Depends(get_db)):
    try:
        print("Request received for last 10 transactions...")  # Debugging
        transactions = get_last_10_transactions(db)  # Fetch the transactions from the database
        print(f"Transactions fetched: {transactions}")  # Debugging
        return transactions  # This will be automatically converted to the response format using Pydantic schemas
    except Exception as e:
        print(f"Error occurred in get_last_10_transactions_endpoint: {e}")  # Debugging
        raise
