import uuid
from pydantic import BaseModel

class TransactionsCategoryBase(BaseModel):
    user_id: uuid.UUID
    category: str
    expense: bool

class TransactionsCategoryCreate(TransactionsCategoryBase):
    pass

class TransactionsCategoryResponse(TransactionsCategoryBase):
    id: uuid.UUID
    class Config:
        orm_mode = True