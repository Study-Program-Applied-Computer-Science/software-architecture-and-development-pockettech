from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SharedTransactionBase(BaseModel):
    transaction_id: UUID
    group_id: UUID
    group_user_id_main: UUID
    group_user_id_sub: UUID
    repayment_transaction_id: Optional[UUID] = None 
    share_value: float
    payment_status: 2

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types (like Decimal)
        orm_mode = True 

class SharedTransactionCreate(BaseModel):
    recording_user_id: UUID
    credit_user_id: Optional[UUID] = None
    debit_user_id: Optional[UUID] = None
    other_party: Optional[str] = None
    heading: str
    description: Optional[str] = None
    transaction_mode: str
    shared_transaction: bool
    category: int
    amount: float
    currency_code: int
    group_id: UUID
    pass



class SharedTransaction(SharedTransactionBase):
    id: UUID

    class Config:
        orm_mode = True
