from sqlalchemy.orm import Session
from app.models.transaction_analysis import Transaction
from datetime import datetime, timedelta
import pytz;
from sqlalchemy.sql import func
from app.models.userTransactionCategory import UserTransactionsCategory

# Fetch the last 10 transactions
def get_last_10_transactions(db: Session):
    try:
        print("Fetching last 10 transactions from the database...")  # Debugging
        query = db.query(
            Transaction.id,
            Transaction.timestamp,
            Transaction.recording_user_id,
            Transaction.heading,
            Transaction.description,
            Transaction.amount,
            Transaction.currency_code,
            Transaction.transaction_mode,
            Transaction.shared_transaction,
            Transaction.category_id
        ).order_by(Transaction.timestamp.desc())  # Order by timestamp
        
        print("SQL Query:", str(query))  # Debugging
        result = query.limit(10).all()  # Fetch last 10 transactions
        print(f"Found {len(result)} transactions.")  # Debugging
        return result
    except Exception as e:
        print(f"Error in get_last_10_transactions: {e}")  # Debugging
        raise


def get_last_week_transactions(db: Session):
    try:
        print("Fetching transactions from the last 7 days...")  # Debugging
        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)  # Make UTC timezone-aware
        seven_days_ago = utc_now - timedelta(days=7)

        print(f"Seven days ago (UTC with tz): {seven_days_ago}")  # Debugging

        query = db.query(
            Transaction.id,
            Transaction.timestamp,
            Transaction.recording_user_id,
            Transaction.heading,
            Transaction.description,
            Transaction.amount,
            Transaction.currency_code,
            Transaction.transaction_mode,
            Transaction.shared_transaction,
            Transaction.category_id
        ).filter(Transaction.timestamp >= seven_days_ago)  # Correct timezone comparison

        print("SQL Query:", str(query))  # Debugging
        result = query.order_by(Transaction.timestamp.desc()).all()
        print(f"Found {len(result)} transactions in the last week.")  # Debugging

        for transaction in result:
            print(f"Transaction ID: {transaction.id}, Timestamp: {transaction.timestamp}")

        return result
    except Exception as e:
        print(f"Error in get_last_week_transactions: {e}")  # Debugging
        raise

def get_expenses_by_category(db: Session):
    try:
        print("Fetching total expenses grouped by category...")

        # Updated query to include category, total_amount, and additional fields
        query = db.query(
            UserTransactionsCategory.category,
            func.sum(Transaction.amount).label("total_amount"),
            Transaction.recording_user_id.label("user_id"),  # Add user_id
            Transaction.id.label("id")  # Add id if necessary
        ).join(
            UserTransactionsCategory, Transaction.category_id == UserTransactionsCategory.id
        ).group_by(
            UserTransactionsCategory.category, Transaction.recording_user_id, Transaction.id
        )  # Group by category and include additional fields

        result = query.all()
        print(f"Found {len(result)} category expenses.")
        return result
    except Exception as e:
        print(f"Error in get_expenses_by_category: {e}")
        raise