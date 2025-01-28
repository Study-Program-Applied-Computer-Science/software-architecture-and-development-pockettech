from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class SharedTransactionBase(BaseModel):
    transaction_id: UUID
    group_user_id_main: UUID
    group_user_id_sub: UUID
    share_type_id: int
    share_value: Decimal
    payment_status: int

class SharedTransactionCreate(SharedTransactionBase):
    pass

class SharedTransaction(SharedTransactionBase):
    id: UUID

    class Config:
        orm_mode = True
