from pydantic import BaseModel
from typing import List, Optional

class UserTransactionsCategoryBase(BaseModel):
    category: str
    expense: bool


class UserTransactionsCategoryCreate(UserTransactionsCategoryBase):
    pass


class UserTransactionsCategoryResponse(UserTransactionsCategoryBase):
    id: int
    total_amount: float  

    class Config:
        orm_mode = True 
