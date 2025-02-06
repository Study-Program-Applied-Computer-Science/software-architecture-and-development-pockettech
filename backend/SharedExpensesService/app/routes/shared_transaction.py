from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import shared_transaction as crud
from uuid import UUID
from app.schemas.shared_transaction import SharedTransaction
from app.schemas.transaction import TransactionCreate 
from app.schemas.shared_transaction import SharedTransactionCreate, SharedTransactionWithName
from app.crud.shared_transaction import create_shared_transaction
from app.crud.shared_transaction import get_transactions_with_names
from app.schemas.country import CountryResponse
from app.schemas.transactionsCategory import UserTransactionsCategoryResponse
from app.crud.shared_transaction import get_all_categories, get_all_currencies
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
    transaction: SharedTransactionCreate,
    db: Session = Depends(get_db)
):
    return create_shared_transaction(db, transaction)

# Get shared transactions by group_user_id_main or group_user_id_sub
@router.get("/shared-transactions/{group_user_id}/{group_id}", response_model=list[SharedTransaction])
def get_transaction_by_group_user_id_route(
    group_user_id: UUID,
    group_id: UUID,
    db: Session = Depends(get_db)
):
    shared_transactions = crud.get_transaction_by_group_user_id(
        db=db,
        group_user_id=group_user_id,
        group_id=group_id
    )
    
    return shared_transactions

#Get names of uuids in shared 
@router.get("/shared-transactions/named/{group_user_id}/{group_id}", response_model=list[SharedTransactionWithName])
def get_transaction_with_names_route(
    group_user_id: UUID,
    group_id: UUID,
    db: Session = Depends(get_db)
):
    return get_transactions_with_names(db, group_user_id, group_id)



@router.get("/categories", response_model=list[UserTransactionsCategoryResponse])
def get_all_categories_route(db: Session = Depends(get_db)):
    #logger.info("Getting all categories")
    try:
        print("Getting all categories", get_all_categories(db))
        return get_all_categories(db)
    except Exception as e:
        #logger.error(f"Failed to get categories: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/currencies", response_model=list[CountryResponse])
def get_all_currencies_route(db: Session = Depends(get_db)):
    # logger.info("Getting all currencies")
    try:
        return get_all_currencies(db)
    except Exception as e:
        # logger.error(f"Failed to get currencies: {e}")
        raise HTTPException(status_code=400, detail=str(e))