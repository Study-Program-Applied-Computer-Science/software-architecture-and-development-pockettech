from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
from app.models.country import Country
import jwt

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.transactionsCategory import TransactionsCategory
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetUpdate
from app.utils.jwt_rsa import create_access_token

from common.config.logging import setup_logger
from common.utils.http_client import make_request
from common.config.correlation import get_correlation_id
from common.config.constants import USER_ROLES, BUDGETING_SERVICE_ROLE, TRANSACTION_SERVICE_URL

load_dotenv()
SERVICE_NAME = os.getenv("SERVICE_NAME")

logger = setup_logger(SERVICE_NAME)


#get all budgets
def get_all_budgets(db: Session):
    query = db.query(
        Budget.id,
        Budget.user_id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        TransactionsCategory.category,
        TransactionsCategory.expense
    ).join(
        TransactionsCategory,
        Budget.category_id == TransactionsCategory.id
    )

    return query.all()


#get a budget by id
def get_budget_by_id(db: Session, budget_id: uuid.UUID):
    query = db.query(
        Budget.id,
        Budget.user_id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        TransactionsCategory.category,
        TransactionsCategory.expense
    ).join(
        TransactionsCategory,
        Budget.category_id == TransactionsCategory.id
    ).filter(
        Budget.id == budget_id
    )
 
    return query.first()


#get all budgets by user_id
def get_all_budgets_by_user_id(db: Session, user_id: uuid.UUID):
    query = db.query(
        Budget.id,
        Budget.user_id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        TransactionsCategory.category,
        TransactionsCategory.expense
    ).join(
        TransactionsCategory,
        Budget.category_id == TransactionsCategory.id
    ).filter(
        Budget.user_id == user_id
    )

    return query.all()


#get all budgets by user_id, start_date, end_date
def get_all_budgets_by_user_id_and_date(db: Session, user_id: uuid.UUID, start_date, end_date):
    query = db.query(
        Budget.id,
        Budget.user_id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        TransactionsCategory.category,
        TransactionsCategory.expense
    ).join(
        TransactionsCategory,
        Budget.category_id == TransactionsCategory.id
    ).filter(
        Budget.user_id == user_id,
        Budget.start_date <= start_date,
        Budget.end_date >= end_date
    )

    return query.all()


#create a budget
def create_budget(db: Session, budget: BudgetCreate):
    db_budget = Budget(
        user_id=budget.user_id,
        category_id=budget.category_id,
        amount=budget.amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
        currency_id=budget.currency_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


#update a budget
def update_budget(db: Session, budget_id: uuid.UUID, budget: BudgetUpdate):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        return None

    for var, value in vars(budget).items():
        if value is not None:
            setattr(db_budget, var, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget


#delete a budget
def delete_budget(db: Session, budget_id: uuid.UUID):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        return None

    db.delete(db_budget)
    db.commit()
    return db_budget


#get all transactions by user_id, category_id, start_date, end_date of all budgets that fall within the date range
#TODO: need to call transaction data from the transaction service
def get_all_transactions_by_user_id_and_date_budgets(db: Session, user_id: uuid.UUID, start_date, end_date):
    budgets_query = db.query(
        Budget.id,
        Budget.user_id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        TransactionsCategory.category,
        TransactionsCategory.expense
    ).join(
        TransactionsCategory,
        Budget.category_id == TransactionsCategory.id
    ).filter(
        Budget.user_id == user_id,
        (Budget.start_date >= start_date) & (Budget.end_date <= end_date)
    )
    budgets = budgets_query.all()
    budgets_transactions = []
    for budget in budgets:

        correlation_id = get_correlation_id()
        logger.info("Transactions details", extra={"correlationId   ": correlation_id})

        budgeting_service_role = [BUDGETING_SERVICE_ROLE]

        budgeting_service_token_payload = {
            "id": BUDGETING_SERVICE_ROLE,
            "roles": budgeting_service_role,
            "iat": int(datetime.now().timestamp())
            }
        
        budgeting_service_token = create_access_token(budgeting_service_token_payload)

        headers = {"Authorization": f"Bearer {budgeting_service_token}",
        "X-Correlation-ID": correlation_id}

        print("headers for auth_service_token",headers)
        transaction_service_response = requests.get(f"{TRANSACTION_SERVICE_URL}/category-date/{user_id}/{budget.category_id}/{start_date}/{end_date}", headers=headers)

        if transaction_service_response.status_code != 200:
            logger.error("Failed to fetch transactions for the budget", extra={"correlationId": correlation_id})
            raise HTTPException(status_code=transaction_service_response.status_code, detail="Failed to fetch transactions")
        
        transactions = transaction_service_response.json()

        # transactions_query = db.query(
        #     Transaction.id,
        #     Transaction.timestamp,
        #     Transaction.recording_user_id,
        #     Transaction.credit_user_id,
        #     Transaction.debit_user_id,
        #     Transaction.other_party,
        #     Transaction.heading,
        #     Transaction.description,
        #     Transaction.transaction_mode,
        #     Transaction.shared_transaction,
        #     Transaction.category,
        #     Transaction.amount,
        #     Transaction.currency_code
        # ).filter(
        #     and_(
        #         Transaction.category == budget.category_id,
        #         or_(
        #             Transaction.debit_user_id == user_id,
        #             Transaction.credit_user_id == user_id
        #         ),
        #         Transaction.timestamp >= start_date,
        #         Transaction.timestamp <= end_date
        #     )
        # )
        # transactions = transactions_query.all()
        transactions_list = []
        total_amount = 0.0
        for transaction in transactions:
            transactions_list.append({
                "transaction_id": transaction.id,
                "timestamp": transaction.timestamp,
                "recording_user_id": transaction.recording_user_id,
                "credit_user_id": transaction.credit_user_id or None,
                "debit_user_id": transaction.debit_user_id or None,
                "other_party": transaction.other_party or None,
                "heading": transaction.heading,
                "description": transaction.description or None,
                "transaction_mode": transaction.transaction_mode,
                "shared_transaction": transaction.shared_transaction,
                "category_id": transaction.category,
                "amount": float(transaction.amount),
                "currency_code": transaction.currency_code
            })
            if budget.expense:
                if transaction.debit_user_id == user_id:
                    total_amount += float(transaction.amount)
                if transaction.credit_user_id == user_id:
                    total_amount -= float(transaction.amount)
            else:
                if transaction.credit_user_id == user_id:
                    total_amount += float(transaction.amount)
                if transaction.debit_user_id == user_id:
                    total_amount -= float(transaction.amount)
        budgets_transactions.append({
            "category_id": budget.category_id,
            "amount": float(budget.amount),
            "start_date": budget.start_date,
            "end_date": budget.end_date,
            "currency_id": budget.currency_id,
            "id": budget.id,
            "user_id": budget.user_id,
            "category": budget.category,
            "expense": budget.expense,
            "transactions": transactions_list,
            "total_amount": total_amount
        })
    return budgets_transactions


def get_all_currencies(db: Session):
    return db.query(Country).all()
 
def get_all_categories(db: Session):
    return db.query(TransactionsCategory).all()