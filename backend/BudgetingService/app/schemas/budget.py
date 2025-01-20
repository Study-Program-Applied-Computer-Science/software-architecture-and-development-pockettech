import uuid
from pydantic import BaseModel
from decimal import Decimal
from datetime import date


class BudgetBase(BaseModel):
    category_id: uuid.UUID
    amount: Decimal
    start_date: date
    end_date: date
    currency_id: uuid.UUID


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BudgetBase):
    amount: Decimal | None = None
    start_date: date | None = None
    end_date: date | None = None


class BudgetResponse(BudgetBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
