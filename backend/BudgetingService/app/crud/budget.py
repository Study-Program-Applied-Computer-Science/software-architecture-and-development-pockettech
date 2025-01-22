import uuid

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.userTransactionsCategory import UserTransactionsCategory
from app.schemas.budget import BudgetCreate, BudgetUpdate


#get all budgets
def get_all_budgets(db: Session):
    query = db.query(
        Budget.id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        UserTransactionsCategory.user_id,
        UserTransactionsCategory.category
    ).join(
        UserTransactionsCategory,
        Budget.category_id == UserTransactionsCategory.id
    )

    return query.all()


#get all budgets by user_id
def get_all_budgets_by_user_id(db: Session, user_id: uuid.UUID):
    query = db.query(
        Budget.id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        UserTransactionsCategory.user_id,
        UserTransactionsCategory.category
    ).join(
        UserTransactionsCategory,
        Budget.category_id == UserTransactionsCategory.id
    ).filter(
        UserTransactionsCategory.user_id == user_id
    )

    return query.all()


#get all budgets by user_id, start_date, end_date
def get_all_budgets_by_user_id_and_date(db: Session, user_id: uuid.UUID, start_date, end_date):
    query = db.query(
        Budget.id,
        Budget.category_id,
        Budget.amount,
        Budget.start_date,
        Budget.end_date,
        Budget.currency_id,
        UserTransactionsCategory.user_id,
        UserTransactionsCategory.category
    ).join(
        UserTransactionsCategory,
        Budget.category_id == UserTransactionsCategory.id
    ).filter(
        UserTransactionsCategory.user_id == user_id,
        Budget.start_date <= start_date,
        Budget.end_date >= end_date
    )

    return query.all()


#create a budget
def create_budget(db: Session, budget: BudgetCreate):
    db_budget = Budget(
        category_id=budget.category_id,
        amount=budget.amount,
        start_date=budget.start_date,
        end_date=budget.end_date,
        currency_id=budget.currency_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


#update a budget
def update_budget(db: Session, budget_id: uuid.UUID, budget: BudgetUpdate):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        return None

    for var, value in vars(budget).items():
        if value is not None:
            setattr(db_budget, var, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget


#delete a budget
def delete_budget(db: Session, budget_id: uuid.UUID):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if db_budget is None:
        return None

    db.delete(db_budget)
    db.commit()
    return db_budget