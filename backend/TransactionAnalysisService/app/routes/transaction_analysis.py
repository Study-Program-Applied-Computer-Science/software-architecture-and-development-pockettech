from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db  # Database session dependency
from app.crud.transaction_analysis import get_last_10_transactions, get_last_week_transactions, get_expenses_by_category  # Import both functions
from app.schemas.transaction_analysis import TransactionResponse  # Pydantic schema
from app.schemas.userTransactionCategory import UserTransactionsCategoryResponse  # Pydantic schema
from typing import List

router = APIRouter()

# API endpoint to get the last 10 transactions
@router.get("/transactions/last-10", response_model=List[TransactionResponse])
def get_last_10_transactions_endpoint(db: Session = Depends(get_db)):
    try:
        print("Request received for last 10 transactions...")  # Debugging
        transactions = get_last_10_transactions(db)  # Fetch transactions
        print(f"Transactions fetched: {transactions}")  # Debugging
        return transactions  # Response model automatically formats the data
    except Exception as e:
        print(f"Error occurred in get_last_10_transactions_endpoint: {e}")
        raise

# API endpoint to get transactions from the last week
@router.get("/transactions/last-week", response_model=List[TransactionResponse])
def get_last_week_transactions_endpoint(db: Session = Depends(get_db)):
    try:
        print("Request received for last week's transactions...")  # Debugging
        transactions = get_last_week_transactions(db)  # Fetch last week's transactions
        print(f"Transactions fetched: {transactions}")  # Debugging
        return transactions
    except Exception as e:
        print(f"Error occurred in get_last_week_transactions_endpoint: {e}")
        raise

# API endpoint to fetch expenses grouped by category
@router.get("/transactions/expenses-by-category", response_model=List[UserTransactionsCategoryResponse])
def get_expenses_by_category_endpoint(db: Session = Depends(get_db)):
    try:
        print("Request received for expenses by category...")  # Debugging
        category_expenses = get_expenses_by_category(db)
        print(f"Expenses fetched: {category_expenses}")  # Debugging
        return category_expenses
    except Exception as e:
        print(f"Error occurred in get_expenses_by_category_endpoint: {e}")
        raise