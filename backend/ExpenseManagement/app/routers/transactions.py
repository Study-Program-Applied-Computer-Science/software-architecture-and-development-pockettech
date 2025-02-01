import uuid


from app.schemas import transaction
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.crud import delete_transaction, get_transactions, get_transaction_by_category_id, get_transaction_by_user_id, get_transaction_by_user_id_date, get_transaction_by_id, create_transaction, update_transaction


router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.get("/", response_model=list[transaction.TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)

@router.get("/{transaction_id}", response_model=transaction.TransactionResponse)
def read_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    db_transaction = get_transaction_by_id(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.get("/user/{user_id}", response_model=list[transaction.TransactionResponse])
def read_transactions_by_user_id(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_transactions = get_transaction_by_user_id(db, user_id)
    if db_transactions is None:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return db_transactions

@router.get("/user/{user_id}/date", response_model=list[transaction.TransactionResponse])
def read_transactions_by_user_id_date(user_id: uuid.UUID, start_date, end_date, db: Session = Depends(get_db)):
    db_transactions = get_transaction_by_user_id_date(db, user_id, start_date, end_date)
    if db_transactions is None or len(db_transactions) == 0:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return db_transactions

@router.get("user/{user_id}/category/{category}/date", response_model=list[transaction.TransactionResponse])
def read_transactions_by_category_id(user_id: uuid.UUID, category_id: int, start_date, end_date, db: Session = Depends(get_db)):
    db_transactions = get_transaction_by_category_id(db, user_id, category_id, start_date, end_date)
    if db_transactions is None or len(db_transactions) == 0:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return db_transactions

@router.post("/", response_model=transaction.TransactionBase)
def create_transaction_endpoint(transaction: transaction.TransactionCreate, db: Session = Depends(get_db)):
    try:    
        new_transcation = create_transaction(db, transaction)
        return new_transcation
    except Exception as e:
        import traceback
        print(f"Database error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{transaction_id}", response_model=transaction.TransactionResponse)    
def update_transaction_endpoint(transaction_id: uuid.UUID, transaction: transaction.TransactionUpdate, db: Session = Depends(get_db)):
    try:
        print("transaction-------------------------------")
        print(transaction)
        print(transaction_id)
        updated_transaction = update_transaction(db, transaction_id, transaction)
        return updated_transaction
    except Exception as e:
        import traceback
        print(f"Database error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{transaction_id}", response_model=transaction.TransactionResponse)
def delete_transaction_endpoint(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        deleted_transaction = delete_transaction(db, transaction_id)
        return deleted_transaction
    except Exception as e:
        import traceback
        print(f"Database error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))