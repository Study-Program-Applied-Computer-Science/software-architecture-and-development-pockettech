import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.budget import BudgetBaseResponse, BudgetCreate, BudgetResponse, BudgetUpdate, Budgets
from app.db.database import get_db
from app.crud.budget import create_budget, delete_budget, get_all_budgets, get_all_budgets_by_user_id, get_all_budgets_by_user_id_and_date, get_all_transactions_by_user_id_and_date_budgets, update_budget


router = APIRouter()


#get all budgets
@router.get("/", response_model=list[BudgetResponse])
def get_all_budgets_route(db: Session = Depends(get_db)):
    return get_all_budgets(db)


#get all budgets of user_id
@router.get("/{user_id}", response_model=list[BudgetResponse])
def get_all_budgets_by_user_id_route(user_id: uuid.UUID, db: Session = Depends(get_db)):
    budgets = get_all_budgets_by_user_id(db, user_id)
    if not budgets:
        raise HTTPException(status_code=404, detail="Budgets not found for this user")
    return budgets


#get all budgets of user id that is valid during the inputted date range
@router.get("/{user_id}/{start_date}/{end_date}", response_model=list[BudgetResponse])
def get_all_budgets_by_user_id_and_date_route(user_id: uuid.UUID, start_date, end_date, db: Session = Depends(get_db)):
    budgets = get_all_budgets_by_user_id_and_date(db, user_id, start_date, end_date)
    if not budgets:
        raise HTTPException(status_code=404, detail="Budgets not found for this user and date range")
    return budgets


#create a budget
@router.post("/", response_model=BudgetBaseResponse)
def create_budget_route(budget: BudgetCreate, db: Session = Depends(get_db)):
    try:
        return create_budget(db, budget)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#update a budget
@router.put("/{id}", response_model=BudgetBaseResponse)
def update_budget_route(id: uuid.UUID, budget: BudgetBaseResponse, db: Session = Depends(get_db)):
    try:
        return update_budget(db, id, budget)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
#delete a budget
@router.delete("/{id}")
def delete_budget_route(id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return delete_budget(db, id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

#route for get_all_transactions_by_user_id_and_date_budgets
@router.get("/alltransactions/{user_id}/{start_date}/{end_date}", response_model=list[Budgets])
def get_all_transactions_by_user_id_and_date_budgets_route(user_id: uuid.UUID, start_date, end_date, db: Session = Depends(get_db)):
    budgets = get_all_transactions_by_user_id_and_date_budgets(db, user_id, start_date, end_date)
    if not budgets:
        raise HTTPException(status_code=404, detail="Budgets not found for this user and date range")
    return budgets