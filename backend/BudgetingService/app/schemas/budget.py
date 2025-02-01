from typing import Optional, List
import uuid
from pydantic import BaseModel
from datetime import date, datetime


class BudgetBase(BaseModel):
    user_id: uuid.UUID
    category_id: int
    amount: float
    start_date: date
    end_date: date
    currency_id: int


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    pass


class BudgetBaseResponse(BudgetBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
        

class BudgetResponse(BudgetBase):
    id: uuid.UUID
    category: str
    expense: bool

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    transaction_id: uuid.UUID
    timestamp: datetime
    recording_user_id: uuid.UUID
    credit_user_id: Optional[uuid.UUID]
    debit_user_id: Optional[uuid.UUID]
    other_party: Optional[str]
    heading: str
    description: Optional[str]
    transaction_mode: str
    shared_transaction: bool
    category_id: int
    amount: float
    currency_code: int

    class Config:
        orm_mode = True


class Budgets(BudgetResponse):
    transactions: List[Transaction]
    total_amount: float

    class Config:
        orm_mode = True
