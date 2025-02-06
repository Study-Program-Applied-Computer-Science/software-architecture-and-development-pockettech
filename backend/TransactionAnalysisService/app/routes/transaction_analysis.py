from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.crud.transaction_analysis import (
    get_last_10_transactions,
    get_last_week_transactions,
    get_expenses_by_category,
    predict_savings,
    categorize_transactions
)
from app.schemas.transaction import TransactionResponse  # Pydantic schema
from app.schemas.transactionCategory import UserTransactionsCategoryResponse  # Pydantic schema
from typing import List
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy.sql import func
from app.models.transaction import Transaction
from app.models.transactionCategory import TransactionsCategory

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


# API endpoint to get the last 10 transactions
@router.get("/transactions/last-10", response_model=List[TransactionResponse])
@limiter.limit("10/minute")
def get_last_10_transactions_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"[{request.client.host}] Fetching last 10 transactions...")
        transactions = get_last_10_transactions(db)
        logger.info(f"Successfully retrieved {len(transactions)} transactions.")
        return transactions
    except Exception as e:
        logger.error(f"Error fetching last 10 transactions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching last 10 transactions.")


# API endpoint to get transactions from the last week
@router.get("/transactions/last-week", response_model=List[TransactionResponse])
@limiter.limit("5/minute")
def get_last_week_transactions_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"[{request.client.host}] Fetching last week's transactions...")
        transactions = get_last_week_transactions(db)
        logger.info(f"Successfully retrieved {len(transactions)} transactions from last week.")
        return transactions
    except Exception as e:
        logger.error(f"Error fetching last week's transactions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching last week's transactions.")


# API endpoint to fetch expenses grouped by category
@router.get("/transactions/expenses-by-category", response_model=List[UserTransactionsCategoryResponse])
@limiter.limit("5/minute")
def get_expenses_by_category_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        logger.info(f"[{request.client.host}] Fetching expenses grouped by category...")
        category_expenses = get_expenses_by_category(db)
        logger.info(f"Successfully retrieved expenses for {len(category_expenses)} categories.")
        return category_expenses
    except Exception as e:
        logger.error(f"Error fetching expenses by category: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching expenses by category.")


# Prediction endpoint
@router.post("/transactions/predict-savings/{user_id}")
@limiter.limit("5/minute")
def predict_savings_endpoint(
    request: Request,
    user_id: UUID,
    months_to_predict: int = 3,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"[{request.client.host}] Predicting savings for User {user_id} for {months_to_predict} months...")
        result = predict_savings(db, user_id, months_to_predict)
        logger.info(f"Savings prediction successful for User {user_id}.")
        return result
    except HTTPException as e:
        logger.warning(f"Prediction failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Savings prediction failed")


# Categorization endpoint
@router.post("/transactions/categorize-transactions")
@limiter.limit("5/minute")
def categorize_transactions_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"[{request.client.host}] Categorizing transactions...")
        result = categorize_transactions(db)
        logger.info("Transaction categorization successful.")
        return result
    except HTTPException as e:
        logger.warning(f"Categorization failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Categorization error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Transaction categorization failed")
