from sqlalchemy.orm import Session
from app.models.transaction_analysis import Transaction

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
            Transaction.shared_transaction,  # Missing field added
            Transaction.category_id          # Missing field added
        ).order_by(Transaction.timestamp.desc()) # Order by timestamp to get the latest transactions
        
        # Print the actual query to see what it's doing
        print("SQL Query:", str(query))  # Debugging
        result = query.limit(10).all()  # Return the query results (which will be SQLAlchemy models)
        print(f"Found {len(result)} transactions.")  # Debugging
        return result
    except Exception as e:
        print(f"Error occurred in get_last_10_transactions: {e}")  # Debugging
        raise
