import uuid
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    country_id: int
    email_id: str
    password: str
    phone_number: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: Optional[str] = None
    email_id: Optional[str] = None
    password: Optional[str] = None
    
class UserResponse(UserBase):
    id: uuid.UUID
    class Config:
        orm_mode = True