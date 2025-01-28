from pydantic import BaseModel
from uuid import UUID

class SharedGroupBase(BaseModel):
    group_name: str

class SharedGroupCreate(SharedGroupBase):
    admin_user_id: UUID

class SharedGroup(SharedGroupBase):
    id: UUID
    admin_user_id: UUID

    class Config:
        orm_mode = True
        from_attributes = True 
