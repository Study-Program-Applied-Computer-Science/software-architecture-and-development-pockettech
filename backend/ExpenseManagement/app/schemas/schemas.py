from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    type: str  # "income" or "expense"
    amount: float
    category: str
    description: str | None = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True