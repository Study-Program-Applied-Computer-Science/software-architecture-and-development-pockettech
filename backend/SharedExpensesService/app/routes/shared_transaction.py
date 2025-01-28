from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import shared_transaction as crud
from app.schemas.shared_transaction import SharedTransactionCreate, SharedTransaction
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=SharedTransaction)
def create_shared_transaction(transaction: SharedTransactionCreate, db: Session = Depends(get_db)):
    return crud.create_shared_transaction(db, transaction)

@router.get("/{transaction_id}", response_model=SharedTransaction)
def get_shared_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    transaction = crud.get_shared_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/group/{group_id}", response_model=list[SharedTransaction])
def get_shared_transactions_by_group(group_id: UUID, db: Session = Depends(get_db)):
    transactions = crud.get_shared_transactions_by_group(db, group_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for the group")
    return transactions

@router.put("/shared-transaction/{transaction_id}", response_model=SharedTransaction)
def update_shared_transaction(transaction_id: UUID, transaction_data: SharedTransactionCreate, db: Session = Depends(get_db)):
    updated_transaction = crud.update_shared_transaction(db, transaction_id, transaction_data)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction


@router.delete("/{transaction_id}", response_model=SharedTransaction)
def delete_shared_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    deleted_transaction = crud.delete_shared_transaction(db, transaction_id)
    if not deleted_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return deleted_transaction