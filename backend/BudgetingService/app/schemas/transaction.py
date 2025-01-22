import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class TransactionBase(BaseModel):
    recording_user_id: uuid.UUID
    credit_user_id: Optional[uuid.UUID] = None
    debit_user_id: Optional[uuid.UUID] = None
    other_party: Optional[str] = None
    heading: str
    description: Optional[str] = None
    transaction_mode: str
    shared_transaction: bool
    category_id: uuid.UUID
    amount: int
    currency_code: uuid.UUID


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        orm_mode = True
