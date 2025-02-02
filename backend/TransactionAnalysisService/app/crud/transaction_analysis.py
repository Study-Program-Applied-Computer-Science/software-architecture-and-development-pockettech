from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from datetime import datetime, timedelta
import pytz
from sqlalchemy.sql import func
from app.models.transactionCategory import TransactionsCategory
from sqlalchemy import Float
from app.schemas.transactionCategory import UserTransactionsCategoryResponse  # Import the response model



# Fetch the last 10 transactions
def get_last_10_transactions(db: Session):
    try:
        print("Fetching last 10 transactions from the database...")

        query = db.query(
            Transaction.id,
            Transaction.timestamp,
            Transaction.recording_user_id,
            Transaction.heading,
            Transaction.description,
            Transaction.amount,  # Return amount without casting to float
            Transaction.currency_code,  # Ensure this is stored as a string
            Transaction.transaction_mode,
            Transaction.shared_transaction,
            Transaction.category  # Use category_id instead of category
        ).order_by(Transaction.timestamp.desc()).limit(10)

        result = query.all()

        # Cast amount to float after fetching data
        result = [
            {
                **transaction._asdict(),  # Convert the SQLAlchemy Row object to a dictionary
                'amount': float(transaction.amount)  # Cast the amount to float here
            }
            for transaction in result
        ]

        print(f"Found {len(result)} transactions.")
        return result
    except Exception as e:
        print(f"Error in get_last_10_transactions: {e}")
        raise

def get_last_week_transactions(db: Session):
    try:
        print("Fetching transactions from the last 7 days...")

        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        seven_days_ago = utc_now - timedelta(days=7)

        print(f"Seven days ago (UTC with tz): {seven_days_ago}")

        query = db.query(
            Transaction.id,
            Transaction.timestamp,
            Transaction.recording_user_id,
            Transaction.heading,
            Transaction.description,
            Transaction.amount,  # Return amount without casting to float
            Transaction.currency_code,  # Ensure string format
            Transaction.transaction_mode,
            Transaction.shared_transaction,
            Transaction.category  # Use category_id
        ).filter(Transaction.timestamp >= seven_days_ago)

        result = query.order_by(Transaction.timestamp.desc()).all()

        # Cast amount to float after fetching data
        result = [
            {
                **transaction._asdict(),  # Convert the SQLAlchemy Row object to a dictionary
                'amount': float(transaction.amount)  # Cast the amount to float here
            }
            for transaction in result
        ]

        print(f"Found {len(result)} transactions in the last week.")
        return result
    except Exception as e:
        print(f"Error in get_last_week_transactions: {e}")
        raise

# Fetch total expenses by category

def get_expenses_by_category(db: Session):
    try:
        print("Fetching total expenses grouped by category...")

        query = db.query(
            TransactionsCategory.id,  # The category ID
            TransactionsCategory.category,  # The category name
            TransactionsCategory.expense,  # Whether it's an expense category or not
            func.sum(func.cast(Transaction.amount, Float)).label("total_amount")  # Sum of transaction amounts
        ).join(
            Transaction, Transaction.category == TransactionsCategory.id  # Joining the Transaction model with TransactionsCategory
        ).group_by(
            TransactionsCategory.id,  # Grouping by category ID
            TransactionsCategory.category,  # Grouping by category name
            TransactionsCategory.expense  # Grouping by expense flag
        )

        result = query.all()

        # Return the mapped result as the Pydantic model
        return [
            UserTransactionsCategoryResponse(
                id=row[0],  # id from TransactionsCategory
                category=row[1],  # category from TransactionsCategory
                expense=row[2],  # expense from TransactionsCategory
                total_amount=row[3]  # total_amount (sum of transaction amounts)
            )
            for row in result
        ]

    except Exception as e:
        print(f"Error in get_expenses_by_category: {e}")
        raise