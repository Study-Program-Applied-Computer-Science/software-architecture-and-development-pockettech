from fastapi import APIRouter, HTTPException, Depends, Header
import jwt
from app.utils.jwt_rsa import create_access_token, verify_token
from app.schemas.auth import LoginRequest
import requests
from common.config.constants import USER_ROLES
from app.config import settings
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/login")
def login_user(login_request: LoginRequest):
    # Call the UserLoginService to validate credential
    print("login_request",login_request)
    print("settings.user_login_service_url",settings.user_login_service_url)
    response = requests.post(
        url=f"{settings.user_login_service_url}",
        json=login_request.model_dump()
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid credentials")
    
    # Create JWT token
    user_data = response.json()

    user_roles = USER_ROLES

    user_payload = {
        "id": user_data["id"], 
        "roles": user_roles,
        "iat": int(datetime.now().timestamp())
    }

    token = create_access_token(data=user_payload)
    print("token created with Login",token)
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verifytoken")
def get_profile(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization.split(" ")[1]  # Assuming the token is in the format "Bearer <token>"
 
    try:
        user_data = verify_token(token)
        return {"user_id": user_data["id"], "roles": user_data["roles"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")