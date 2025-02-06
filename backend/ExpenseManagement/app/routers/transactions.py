from datetime import datetime
from typing import Optional
import uuid
import requests


from app.schemas import transaction, transactionsCategory, country, user
from app.utils.verifyToken import verify_roles
from app.utils.jwt_rsa import create_access_token
from common.config.constants import USER_ROLES, BUDGETING_SERVICE_ROLE, SHARED_EXPENSES_SERVICE_ROLE, EXPENSE_MANAGEMENT_SERVICE_ROLE, USER_LOGIN_SERVICE_URL
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.crud import get_transaction_by_category_id_user_id_start_date_end_date, get_users, get_countries, get_categories, delete_transaction, get_transactions, get_transaction_by_category_id, get_transaction_by_user_id, get_transaction_by_user_id_date, get_transaction_by_id, create_transaction, update_transaction


router = APIRouter()

@router.get("/category", response_model=list[transactionsCategory.TransactionsCategoryResponse])
def read_transactions_category(db: Session = Depends(get_db)):
    return get_categories(db)

@router.get("/country", response_model=list[country.CountryResponse])
def read_countries(db: Session = Depends(get_db)):
    return get_countries(db)

@router.get("/users", response_model=list[user.UserResponse])
def read_users(db: Session = Depends(get_db)):
    expense_management_service_role = [EXPENSE_MANAGEMENT_SERVICE_ROLE]

    expense_managements_service_token_payload = {
            "id": EXPENSE_MANAGEMENT_SERVICE_ROLE,
            "roles": expense_management_service_role,
            "iat": int(datetime.now().timestamp())
            }
        
    expense_management_service_token = create_access_token(expense_managements_service_token_payload)

    headers = {"Authorization": f"Bearer {expense_management_service_token}"}

    user_login_service_response = requests.get(f"{USER_LOGIN_SERVICE_URL}/", headers=headers)

    if user_login_service_response.status_code != 200:
        raise HTTPException(status_code=user_login_service_response.status_code, detail="Failed to fetch users")
        
    users = user_login_service_response.json()
    return users(db)

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
def read_transactions_by_user_id(user_id: uuid.UUID, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token not found")
    
    # Split the "Bearer <token>" and get the token
    token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else None
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    verify_roles(token, [BUDGETING_SERVICE_ROLE, SHARED_EXPENSES_SERVICE_ROLE, USER_ROLES])

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
def create_transaction_endpoint(transaction: transaction.TransactionCreate, db: Session = Depends(get_db),authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token not found")
    
    # Split the "Bearer <token>" and get the token
    token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else None
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    verify_roles(token, [BUDGETING_SERVICE_ROLE, SHARED_EXPENSES_SERVICE_ROLE, USER_ROLES])
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
def delete_transaction_endpoint(transaction_id: uuid.UUID, db: Session = Depends(get_db), request: Request = None):
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        token_data = verify_roles(token, [USER_ROLES])
        print("data",token_data)
        print("data: ",token_data["id"])
        print("URL ",str(transaction_id))
        if str(token_data["id"]) != str(transaction_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    try:
        deleted_transaction = delete_transaction(db, transaction_id)
        return deleted_transaction
    except Exception as e:
        import traceback
        print(f"Database error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/category-date/{user_id}/{category_id}/{start_date}/{end_date}", response_model=list[transaction.TransactionResponse])
def read_transactions_by_category_id_date(user_id: uuid.UUID, category_id: int, start_date, end_date, db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token not found")
    
    # Split the "Bearer <token>" and get the token
    token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else None
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    verify_roles(token, [BUDGETING_SERVICE_ROLE, SHARED_EXPENSES_SERVICE_ROLE])
    
    try:
        db_transactions = get_transaction_by_category_id_user_id_start_date_end_date(db, user_id, category_id, start_date, end_date)
        return db_transactions
    except Exception as e:
        import traceback
        print(f"Database error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))