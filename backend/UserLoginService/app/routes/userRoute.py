from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.userLogin import UserCreate, UserResponse, LoginRequest
from app.utils.hash import hash_password, verify_password
from app.db.database import get_db
from app.models.country import Country
from app.utils.verifyToken import verify_token_via_api



router = APIRouter()

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email or phone number is already registered
    existing_user = db.query(User).filter((User.email_id == user.email_id)).first()
    print("existing_user",existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone number already registered")

    # Query the Country table to get the phone_code based on the country_id
    print("Checking for country_id:", user.country_id)
    country = db.query(Country).filter(Country.id == user.country_id).first()
    print("Country result:", country)
    
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
def get_all_users(db: Session = Depends(get_db)):
    print("---------------------get_all_users-------------------")
    users = db.query(User).all()
    return users

#get user details
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db), authorization: Optional[str] = Header(None), request: Request = None):
    print("Request Headers:", request.headers)
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        token = authorization
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        user_data = verify_token_via_api(token)
        print("user_data",user_data)
        print("user_data: ",user_data["user_id"])
        print("URL ",str(user_id))
        if str(user_data["user_id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# update user details
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user: UserCreate, db: Session = Depends(get_db), authorization: Optional[str] = Header(None), request: Request = None):
    print("Request Headers:", request.headers)
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        token = authorization
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        user_data = verify_token_via_api(token)
        print("user_data",user_data)
        print("user_data: ",user_data["user_id"])
        print("URL ",str(user_id))
        if str(user_data["user_id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user.name
    user.email_id = user.email_id
    user.password = user.password
    user.country_id = user.country_id
    user.phone_number = user.phone_number
    db.commit()
    db.refresh(user)
    return user

# delete user 
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: UUID, db: Session = Depends(get_db), authorization: Optional[str] = Header(None), request: Request = None):
    print("Request Headers:", request.headers)
    # Try to get the token from cookies
    token = request.cookies.get("access_token")
    
    # Fall back to the Authorization header if the cookie is not available
    if not token:
        token = authorization
        if not token:
            raise HTTPException(status_code=401, detail="Token not found")
    
    print("Token from frontend:", token)
   
    try:
        print("token",token)
        user_data = verify_token_via_api(token)
        print("user_data",user_data)
        print("user_data: ",user_data["user_id"])
        print("URL ",str(user_id))
        if str(user_data["user_id"]) != str(user_id):
            raise HTTPException(status_code=403, detail="Token does not match user ID")
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user