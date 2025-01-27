from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.schemas import TransactionCreate

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session):
    return db.query(Transaction).all()