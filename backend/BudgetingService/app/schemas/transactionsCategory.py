from pydantic import BaseModel


class TransactionsCategoryBase(BaseModel):
    category: str
    expense: bool


class TransactionsCategoryCreate(TransactionsCategoryBase):
    pass


class TransactionsCategoryResponse(TransactionsCategoryBase):
    id: int
 
    class Config:
        orm_mode = True