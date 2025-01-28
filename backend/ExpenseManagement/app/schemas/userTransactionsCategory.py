import uuid
from pydantic import BaseModel

class UserTransactionsCategoryBase(BaseModel):
    user_id: uuid.UUID
    category: str
    expense: bool

class UserTransactionsCategoryCreate(UserTransactionsCategoryBase):
    pass

class UserTransactionsCategoryResponse(UserTransactionsCategoryBase):
    id: uuid.UUID
    class Config:
        orm_mode = True