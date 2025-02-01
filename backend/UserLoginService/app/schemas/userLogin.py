from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_id: EmailStr
    password: str
    country_id: int
    phone_number: str

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email_id: str
    phone_code: str
    phone_number: str

    class Config:
        orm_mode = True
        json_encoders = {UUID: lambda v: str(v)}

class LoginRequest(BaseModel):
    email_id: EmailStr
    password: str

class LoginResponse(BaseModel):
    id: UUID

    class Config:
        json_encoders = {UUID: lambda v: str(v)}
    
