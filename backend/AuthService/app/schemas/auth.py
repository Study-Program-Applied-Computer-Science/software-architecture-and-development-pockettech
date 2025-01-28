from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email_id: EmailStr
    password: str
