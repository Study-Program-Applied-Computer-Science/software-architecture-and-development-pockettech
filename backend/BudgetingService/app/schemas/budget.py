from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import date


class BudgetBase(BaseModel):
    category_id: uuid.UUID
    amount: float
    start_date: date
    end_date: date
    currency_id: int


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    pass


class BudgetResponse(BudgetBase):
    id: uuid.UUID
    user_id: uuid.UUID
    category: str

    class Config:
        orm_mode = True
