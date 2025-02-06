from pydantic import BaseModel


class UserTransactionsCategoryBase(BaseModel):
    category: str
    expense: bool


class UserTransactionsCategoryCreate(UserTransactionsCategoryBase):
    pass


class UserTransactionsCategoryResponse(UserTransactionsCategoryBase):
    id: int

    class Config:
        orm_mode = True