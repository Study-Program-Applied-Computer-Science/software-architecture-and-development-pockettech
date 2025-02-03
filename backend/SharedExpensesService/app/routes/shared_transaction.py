from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import shared_transaction as crud
from uuid import UUID
from app.schemas.shared_transaction import SharedTransaction
from app.schemas.transaction import TransactionCreate 
from app.schemas.shared_transaction import SharedTransactionCreate
from app.crud.shared_transaction import create_shared_transaction

router = APIRouter()

# Update a shared transaction
@router.put("/repay_shared_transaction/{shared_transaction_id}", response_model=SharedTransaction)
def repay_shared_transaction(
    shared_transaction_id: UUID,
    db: Session = Depends(get_db)
):
    updated_shared_transaction = crud.update_repayment_transaction(
        db=db,
        shared_transaction_id=shared_transaction_id
    )
    
    return updated_shared_transaction

# Create a shared transaction
@router.post("/shared-transactions/", response_model=list[SharedTransaction])
def create_shared_transaction_route(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db)
):
    return create_shared_transaction(db, transaction)

# Get shared transactions by group_user_id_main or group_user_id_sub
@router.get("/shared-transactions/{group_user_id}", response_model=list[SharedTransaction])
def get_transaction_by_group_user_id_route(
    group_user_id: UUID,
    db: Session = Depends(get_db)
):
    shared_transactions = crud.get_transaction_by_group_user_id(
        db=db,
        group_user_id=group_user_id
    )
    
    return shared_transactions