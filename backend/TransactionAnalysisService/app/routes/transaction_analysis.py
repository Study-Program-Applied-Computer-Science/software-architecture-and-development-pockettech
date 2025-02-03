from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db  # Database session dependency
from app.crud.transaction_analysis import get_last_10_transactions, get_last_week_transactions, get_expenses_by_category  # Import functions
from app.schemas.transaction import TransactionResponse  # Pydantic schema
from app.schemas.transactionCategory import UserTransactionsCategoryResponse  # Pydantic schema
from typing import List
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

# Initialize logger for debugging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# API endpoint to get the last 10 transactions
@router.get("/transactions/last-10", response_model=List[TransactionResponse])
@limiter.limit("10/minute")  # Allow 10 requests per minute
def get_last_10_transactions_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info("Request received for last 10 transactions...")  # Logging
        transactions = get_last_10_transactions(db)  # Fetch transactions
        logger.info(f"Transactions fetched: {transactions}")  # Logging
        return transactions  # Response model automatically formats the data
    except Exception as e:
        logger.error(f"Error occurred in get_last_10_transactions_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error fetching last 10 transactions.")

# API endpoint to get transactions from the last week
@router.get("/transactions/last-week", response_model=List[TransactionResponse])
@limiter.limit("5/minute")  # Allow 5 requests per minute
def get_last_week_transactions_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info("Request received for last week's transactions...")  # Logging
        transactions = get_last_week_transactions(db)  # Fetch last week's transactions
        logger.info(f"Transactions fetched: {transactions}")  # Logging
        return transactions
    except Exception as e:
        logger.error(f"Error occurred in get_last_week_transactions_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error fetching last week's transactions.")

# API endpoint to fetch expenses grouped by category
@router.get("/transactions/expenses-by-category", response_model=List[UserTransactionsCategoryResponse])
@limiter.limit("5/minute")  # Allow 5 requests per minute
def get_expenses_by_category_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info("Request received for expenses by category...")  # Logging
        category_expenses = get_expenses_by_category(db)  # Fetch category expenses
        logger.info(f"Expenses fetched: {category_expenses}")  # Logging
        return category_expenses
    except Exception as e:
        logger.error(f"Error occurred in get_expenses_by_category_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error fetching expenses by category.")