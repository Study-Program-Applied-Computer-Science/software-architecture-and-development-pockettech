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
    country = db.query(Country).filter(Country.id == user.country_id).first()
    
    if not country:
        raise HTTPException(status_code=400, detail="Invalid country_id")
    # Hash the password
    hashed_pw = hash_password(user.password)

    # Create new user
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email_id=user.email_id,
        password=hashed_pw,
        country_id=user.country_id,
        phone_code=country.phone_code,
        phone_number=user.phone_number,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/verifyuser")

def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    print("login_request",login_request)

    user = db.query(User).filter(User.email_id == login_request.email_id).first()
   
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(login_request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # send id in response payload
    return {"id": user.id}

#get user details
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db), authorization: Optional[str] = Header(None), request: Request = None):
    print("Request Headers:", request.headers)
   
    try:
        print("token",authorization)
        user_data = verify_token_via_api(authorization)
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