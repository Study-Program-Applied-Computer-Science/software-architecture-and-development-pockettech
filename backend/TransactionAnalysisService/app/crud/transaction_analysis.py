from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from datetime import datetime, timedelta
import pytz
from sqlalchemy.sql import func
from app.models.transactionCategory import TransactionsCategory
from sqlalchemy import Float
from app.schemas.transactionCategory import UserTransactionsCategoryResponse  # Import the response model
import numpy as np



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
            Transaction.amount, 
            Transaction.currency_code,  
            Transaction.transaction_mode,
            Transaction.shared_transaction,
            Transaction.category 
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


# Predict future savings for a user
def predict_savings(db: Session, user_id: str, months_to_predict: int = 3):
    try:
        print(f"Predicting savings for user {user_id}...")

        # Get last 12 months of transactions for the user
        one_year_ago = datetime.utcnow() - timedelta(days=365)
        transactions = db.query(
            Transaction.amount, Transaction.timestamp
        ).filter(
            Transaction.recording_user_id == user_id,
            Transaction.timestamp >= one_year_ago
        ).all()

        if not transactions:
            return {"error": "No transaction data available."}

        # Aggregate spending per month
        monthly_expenses = {}
        for txn in transactions:
            month_key = txn.timestamp.strftime("%Y-%m")  # YYYY-MM format
            monthly_expenses[month_key] = monthly_expenses.get(month_key, 0) + float(txn.amount)

        # Convert to time series
        expense_values = np.array(list(monthly_expenses.values()))
        months = np.arange(len(expense_values))

        # Predict using linear regression
        slope, intercept = np.polyfit(months, expense_values, 1)
        predictions = {
            f"Month {i+1}": round(intercept + slope * (len(months) + i), 2)
            for i in range(months_to_predict)
        }

        return {"user_id": user_id, "predicted_savings": predictions}

    except Exception as e:
        print(f"Error in predict_savings: {e}")
        return {"error": "Error in savings prediction."}


# Categorize uncategorized transactions
def categorize_transactions(db: Session):
    try:
        print("Categorizing uncategorized transactions...")

        # Fetch transactions that are marked as "Uncategorized" (using our special placeholder 999)
        uncategorized_transactions = db.query(Transaction).filter(Transaction.category == 999).all()

        if not uncategorized_transactions:
            return {"error": "No uncategorized transactions found."}

        # Mapping from transaction description to category names.
        CATEGORY_MAPPING = {
            "Starbucks": "Food & Beverage",
            "Uber": "Transport",
            "Netflix": "Entertainment",
            "Amazon": "Shopping",
        }

        categorized_transactions = []

        for txn in uncategorized_transactions:
            # Assign a category based on the transaction description
            category_name = CATEGORY_MAPPING.get(txn.description, "Uncategorized")

            # Fetch the category ID from TransactionsCategory table (excluding our placeholder)
            category_obj = db.query(TransactionsCategory).filter(
                TransactionsCategory.category == category_name,
                TransactionsCategory.id != 999  # Ensure it's not our placeholder
            ).first()

            if not category_obj:
                # If the category is not found, create it
                category_obj = TransactionsCategory(category=category_name, expense=True)
                db.add(category_obj)
                db.commit()
                db.refresh(category_obj)

            # Update the transaction with the new category ID
            txn.category = category_obj.id

            # Append the result for reporting
            categorized_transactions.append({"id": str(txn.id), "category": category_name})

        db.commit()
        return {"categorized_transactions": categorized_transactions}

    except Exception as e:
        print(f"Error in categorize_transactions: {e}")
        return {"error": "Error in categorizing transactions."}