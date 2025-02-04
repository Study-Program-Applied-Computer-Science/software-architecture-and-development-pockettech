import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.transaction import Transaction
from app.models.transactionCategory import TransactionsCategory
from app.db.database import Base
from app.crud.transaction_analysis import (
    get_last_10_transactions,
    get_last_week_transactions,
    get_expenses_by_category,
)
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use PostgreSQL test database from .env
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fin_user:password@localhost:5432/finance_management")

# Create test database engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for each test."""
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    db = TestingSessionLocal()
    yield db
    db.rollback()  # Rollback to prevent data leaks between tests
    db.close()
    Base.metadata.drop_all(bind=engine)  # Clean up after each test

# Helper function to add dummy transactions
def add_dummy_transactions(db):
    transactions = [
        Transaction(
            timestamp=datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(days=i),
            recording_user_id=i,
            heading=f"Test Transaction {i}",
            description="Test Description",
            amount=100 + i,
            currency_code="USD",
            transaction_mode="card",
            shared_transaction=False,
            category=1,  # Reference to TransactionsCategory
        )
        for i in range(15)
    ]
    db.add_all(transactions)
    db.commit()

# Helper function to add dummy categories
def add_dummy_categories(db):
    categories = [
        TransactionsCategory(id=1, category="Food", expense=True),
        TransactionsCategory(id=2, category="Transport", expense=True),
    ]
    db.add_all(categories)
    db.commit()

# ✅ Test fetching last 10 transactions
def test_get_last_10_transactions(db_session):
    add_dummy_transactions(db_session)
    transactions = get_last_10_transactions(db_session)

    assert len(transactions) == 10  # Should return only the last 10
    assert transactions[0]["heading"] == "Test Transaction 0"  # Most recent transaction

# ✅ Test fetching transactions from the last week
def test_get_last_week_transactions(db_session):
    add_dummy_transactions(db_session)
    transactions = get_last_week_transactions(db_session)

    assert len(transactions) > 0  # Should return transactions
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    assert all(now - txn["timestamp"] <= timedelta(days=7) for txn in transactions)

# ✅ Test fetching total expenses by category
def test_get_expenses_by_category(db_session):
    add_dummy_categories(db_session)
    add_dummy_transactions(db_session)

    expenses = get_expenses_by_category(db_session)

    assert len(expenses) > 0  # Should return at least one category
    assert expenses[0].category == "Food"  # Ensure correct category
