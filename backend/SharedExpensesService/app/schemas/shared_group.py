from pydantic import BaseModel
from uuid import UUID


class SharedGroupBase(BaseModel):
    group_name: str

    class Config:
        orm_mode = True

class SharedGroupCreate(SharedGroupBase):
    user_id: UUID 

    class Config:
        orm_mode = True  

class SharedGroup(SharedGroupBase):
    id: UUID  

    class Config:
        orm_mode = True
