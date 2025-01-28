from sqlalchemy.orm import Session
from app.models.shared_transaction import SharedTransaction
from app.schemas.shared_transaction import SharedTransactionCreate
from uuid import UUID


def create_shared_transaction(db: Session, transaction: SharedTransactionCreate):
    db_transaction = SharedTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_shared_transaction(db: Session, transaction_id: UUID):
    return db.query(SharedTransaction).filter(SharedTransaction.id == transaction_id).first()

def get_shared_transactions_by_group(db: Session, group_id: UUID):
    return db.query(SharedTransaction).filter(
        (SharedTransaction.group_user_id_main == group_id) | (SharedTransaction.group_user_id_sub == group_id)
    ).all()


def update_shared_transaction(db: Session, transaction_id: UUID, updated_data: SharedTransactionCreate):
    # Fetch the transaction by its transaction_id
    transaction = db.query(SharedTransaction).filter(SharedTransaction.transaction_id == transaction_id).first()
    if not transaction:
        return None  # Return None if not found
    
    # Update fields
    for key, value in updated_data.dict().items():
        setattr(transaction, key, value)
    
    db.commit()
    db.refresh(transaction)
    return transaction


def delete_shared_transaction(db: Session, transaction_id: UUID):
    transaction = db.query(SharedTransaction).filter(SharedTransaction.id == transaction_id).first()
    if not transaction:
        return None
    db.delete(transaction)
    db.commit()
    return transaction
