from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SharedTransactionBase(BaseModel):
    transaction_id: UUID
    group_user_id_main: UUID
    group_user_id_sub: UUID
    repayment_transaction_id: Optional[UUID] = None 
    share_value: float
    payment_status: 2

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types (like Decimal)
        orm_mode = True 

class SharedTransactionCreate(SharedTransactionBase):
    pass



class SharedTransaction(SharedTransactionBase):
    id: UUID

    class Config:
        orm_mode = True
