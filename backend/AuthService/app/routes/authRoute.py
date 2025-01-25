from fastapi import APIRouter, HTTPException, Depends
from app.utils.jwt_rsa import create_access_token, verify_token
from app.schemas.auth import LoginRequest
import requests
from app.config import settings

router = APIRouter()

@router.post("/login")
def login_user(login_request: LoginRequest):
    # Call the UserLoginService to validate credentials
    response = requests.post(
        url=f"{settings.user_login_service_url}",
        json=login_request.model_dump()
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid credentials")
    
    # Create JWT token
    user_data = response.json()
    print(user_data)
    token = create_access_token(data={"sub": user_data["id"]})
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
def get_profile(token: str):
    try:
        user_data = verify_token(token)
        return {"user_id": user_data["sub"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
