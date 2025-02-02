from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
import re

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_id: EmailStr
    password: str
    country_id: int
    phone_number: str 

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        error_message = (
            "Password must be 8-20 characters long, include at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character (@$!%*?&)"
        )

        if not (8 <= len(value) <= 20 and
                re.search(r"[A-Z]", value) and
                re.search(r"[a-z]", value) and
                re.search(r"\d", value) and
                re.search(r"[@$!%*?&]", value)):
            raise ValueError(error_message)

        return value



class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email_id: str
    phone_code: str
    phone_number: str
    password: str

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
    
