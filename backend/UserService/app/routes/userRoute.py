from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.userLogin import UserCreate, UserResponse, PublicUserResponse, UserUpdate
from app.utils.hash import hash_password, verify_password
from app.db.database import get_db
from app.models.country import Country
from app.utils.verifyToken import verify_roles
from common.config.constants import USER_ROLES, AUTH_SERVICE_ROLE
from fastapi import Response
from dotenv import dotenv_values

from common.config.logging import setup_logger
from common.utils.http_client import make_request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse



router = APIRouter()

SERVICE_NAME = dotenv_values(".env")["SERVICE_NAME"]
logger = setup_logger(SERVICE_NAME)

# Initialize rate limiter (in-memory)
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=UserResponse, status_code=201)
@limiter.limit("10/minute") 
def register_user(request: Request,user: UserCreate, db: Session = Depends(get_db)):
    # Check if email or phone number is already registered
    existing_user = db.query(User).filter((User.email_id == user.email_id)).first()
    print("existing_user",existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone number already registered")

    # Query the Country table to get the phone_code based on the country_id
    country = db.query(Country).filter(Country.id == user.country_id).first()
    
    if not country:
        raise HTTPException(status_code=400, detail="Invalid country_id")
    # Hash the password
    hashed_pw = hash_password(user.password)

    # Create new user
    new_user = User(
        name=user.name,
        email_id=user.email_id,
        password=hashed_pw,
        country_id=user.country_id,
        phone_number=user.phone_number,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get all users
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db), 
    authorization: Optional[str] = Header(None), 
    x_correlation_id: Optional[str] = Header(None)):
    print("Authorization Header GetALL:", authorization)
    logger.info(f"Received request with Correlation ID: {x_correlation_id}")
    if not authorization:
        logger.error("Token not found", extra={"correlationId": x_correlation_id})
        raise HTTPException(status_code=401, detail="Token not found")
    
    # Split the "Bearer <token>" and get the token
    token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else None
    
    if not token:
        logger.error("Invalid token format", extra={"correlationId": x_correlation_id})
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    verify_roles(token, [AUTH_SERVICE_ROLE])
    users = db.query(User).all()
    return users

#get user details
@router.get("/{user_id}", response_model=PublicUserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db), authorization: Optional[str] = Header(None), request: Request = None):
    print("Request Headers:", request.headers)
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        token = authorization.split("Bearer ")[-1] if "Bearer " in authorization else None
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        token_data = verify_roles(token, [USER_ROLES])
        print("user_data",token_data)
        print("user_data: ",token_data["id"])
        print("URL ",str(user_id))
        if str(token_data["id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_response = user.__dict__.copy()  
    user_response.pop("password", None)  
    
    return user_response


# update user details
@router.put("/{user_id}", response_model=PublicUserResponse)
@limiter.limit("5/minute") 
def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db), request: Request = None):
    print("Request Headers PUT---------------------------:", request.headers)
    print("Request Body PUT---------------------------:", user)
    print("Request Body PUT---------------------------:", request.body())
    
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend PUT-----------------------------:", token)
   
    try:
        print("PUT --------------- token",token)
        token_data = verify_roles(token, [USER_ROLES])
        print("user_data put-------------------------",token_data)
        print("user_data put---------------------: ",token_data["id"])
        print("URL -------------------------------- ",str(user_id))
        if str(token_data["id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_db.name = user.name
    user_db.email_id = user.email_id
    # check if password not null
    if user.password:
        user_db.password = hash_password(user.password)
    #user_db.password = user.password
    #user_db.country_id = user.country_id
    user_db.phone_number = user.phone_number
    db.commit()
    db.refresh(user_db)

    return PublicUserResponse(
    id=user_db.id,
    name=user_db.name,
    email_id=user_db.email_id,
    phone_number=user_db.phone_number
    )


# delete user 
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db), request: Request = None):
    print("Request Headers:", request.headers)
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        token_data = verify_roles(token, [USER_ROLES])
        print("user_data",token_data)
        print("user_data: ",token_data["id"])
        print("URL ",str(user_id))
        if str(token_data["id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=204)  # No Content