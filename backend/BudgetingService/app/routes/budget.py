import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.budget import BudgetBaseResponse, BudgetCreate, BudgetResponse, BudgetUpdate, Budgets
from app.db.database import get_db
from app.crud.budget import create_budget, delete_budget, get_all_budgets, get_all_budgets_by_user_id, get_all_budgets_by_user_id_and_date, get_all_transactions_by_user_id_and_date_budgets, update_budget
from app.utils.logging import setup_logger

router = APIRouter()

logger = setup_logger()

#get all budgets
@router.get("/", response_model=list[BudgetResponse])
def get_all_budgets_route(db: Session = Depends(get_db)):
    logger.info("Getting all budgets")
    try:
        return get_all_budgets(db)
    except Exception as e:
        logger.error(f"Failed to get budgets: {e}")
        raise HTTPException(status_code=400, detail=str(e))


#get all budgets of user_id
@router.get("/{user_id}", response_model=list[BudgetResponse])
def get_all_budgets_by_user_id_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    logger.info(f"Getting all budgets for user_id: {user_id}")
    try:
        budgets = get_all_budgets_by_user_id(db, user_id)
    except Exception as e:
        logger.error(f"Failed to get budgets: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    if not budgets:
        logger.error(f"Budgets not found for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="Budgets not found for this user")
    return budgets


#get all budgets of user id that is valid during the inputted date range
@router.get("/{user_id}/{start_date}/{end_date}", response_model=list[BudgetResponse])
def get_all_budgets_by_user_id_and_date_route(user_id: uuid.UUID, start_date, end_date, db: Session = Depends(get_db)):
    logger.info(f"Getting all budgets for user_id: {user_id} and date range: {start_date} to {end_date}")
    try:
        budgets = get_all_budgets_by_user_id_and_date(db, user_id, start_date, end_date)
    except Exception as e:
        logger.error(f"Failed to get budgets: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    if not budgets:
        logger.error(f"Budgets not found for user_id: {user_id} and date range: {start_date} to {end_date}")
        raise HTTPException(status_code=404, detail="Budgets not found for this user and date range")
    return budgets


#create a budget
@router.post("/", response_model=BudgetBaseResponse)
def create_budget_route(budget: BudgetCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating budget: {budget}")
        return create_budget(db, budget)
    except Exception as e:
        logger.error(f"Failed to create budget: {e}")
        raise HTTPException(status_code=400, detail=str(e))


#update a budget
@router.put("/{id}", response_model=BudgetBaseResponse)
def update_budget_route(id: uuid.UUID, budget: BudgetBaseResponse, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating budget with id: {id}")
        return update_budget(db, id, budget)
    except Exception as e:
        logger.error(f"Failed to update budget: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    
#delete a budget
@router.delete("/{id}")
def delete_budget_route(id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting budget with id: {id}")
        return delete_budget(db, id)
    except Exception as e:
        logger.error(f"Failed to delete budget: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    

#route for get_all_transactions_by_user_id_and_date_budgets
@router.get("/alltransactions/{user_id}/{start_date}/{end_date}", response_model=list[Budgets])
def get_all_transactions_by_user_id_and_date_budgets_route(user_id: uuid.UUID, start_date, end_date, db: Session = Depends(get_db)):
    logger.info(f"Getting all transactions for user_id: {user_id} and date range: {start_date} to {end_date}")
    try:
        budgets = get_all_transactions_by_user_id_and_date_budgets(db, user_id, start_date, end_date)
    except Exception as e:
        logger.error(f"Failed to get budgets: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    if not budgets:
        logger.error(f"Budgets not found for user_id: {user_id} and date range: {start_date} to {end_date}")
        raise HTTPException(status_code=404, detail="Budgets not found for this user and date range")
    return budgets