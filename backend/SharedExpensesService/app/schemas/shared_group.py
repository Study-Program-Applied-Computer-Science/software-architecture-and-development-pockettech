from pydantic import BaseModel
from uuid import UUID

class SharedGroupCreate(BaseModel):
    group_name: str  

    class Config:
        orm_mode = True  

class SharedGroup(SharedGroupCreate):
    id: UUID  

    class Config:
        orm_mode = True
