from fastapi import APIRouter, HTTPException, Depends, Header, Response
import jwt
from app.utils.jwt_rsa import create_access_token
from app.schemas.auth import LoginRequest
import requests
from common.config.constants import USER_ROLES, AUTH_SERVICE_ROLE
from app.config import settings
from datetime import datetime
from app.utils.verify_password import verify_password

from common.config.logging import setup_logger
from common.utils.http_client import make_request
from common.config.correlation import get_correlation_id

router = APIRouter()

SERVICE_NAME = settings.service_name
logger = setup_logger(SERVICE_NAME)


@router.post("/login")
def login_user(login_request: LoginRequest, response: Response):
    # Call the UserLoginService to validate credential
    correlation_id = get_correlation_id()
    logger.info("User Login", extra={"correlationId": correlation_id})
    
    auth_service_role = [AUTH_SERVICE_ROLE]

    auth_service_token_payload = {
        "id": AUTH_SERVICE_ROLE, 
        "roles": auth_service_role,
        "iat": int(datetime.now().timestamp())
    }

    auth_service_token = create_access_token(data=auth_service_token_payload)

    headers = {"Authorization": f"Bearer {auth_service_token}",
        "X-Correlation-ID": correlation_id}

    print("headers for auth_service_token",headers)
    user_service_response = requests.get(f"{settings.user_login_service_url}", headers=headers)

    #user_service_response = make_request("GET", f"{settings.user_login_service_url}", headers=headers)
    
    if user_service_response.status_code != 200:
        logger.error("Failed to fetch users", extra={"correlationId": correlation_id})
        raise HTTPException(status_code=user_service_response.status_code, detail="Failed to fetch users")
    

    users = user_service_response.json()
    user = next((u for u in users if u["email_id"] == login_request.email_id), None)
    
    if not user:
        logger.error("User not found", extra={"correlationId": correlation_id})
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify password using bcrypt
    if not verify_password(login_request.password, user["password"]):
        logger.error("Invalid credentials", extra={"correlationId": correlation_id})
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token
    user_roles = [USER_ROLES]
    

    user_payload = {
        "id": user["id"], 
        "roles": user_roles,
        "iat": int(datetime.now().timestamp())
    }

    token = create_access_token(data=user_payload)

    # Set the token in an HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,    # Prevent JavaScript from accessing the cookie
        samesite="strict" # Prevent CSRF
    )
    
    return {"access_token": token, "token_type": "bearer","id": user["id"]}
