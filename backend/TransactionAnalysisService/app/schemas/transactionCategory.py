from pydantic import BaseModel
from typing import List, Optional

class UserTransactionsCategoryBase(BaseModel):
    category: str
    expense: bool


class UserTransactionsCategoryCreate(UserTransactionsCategoryBase):
    pass


class UserTransactionsCategoryResponse(UserTransactionsCategoryBase):
    id: int
    total_amount: float  # Add total_amount here to represent the sum of transaction amounts.

    class Config:
        orm_mode = True  # This ensures SQLAlchemy models are properly serialized into Pydantic models
