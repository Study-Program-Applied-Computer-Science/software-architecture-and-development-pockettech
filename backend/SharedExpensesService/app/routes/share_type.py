from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import share_type as crud
from app.schemas.share_type import ShareTypeCreate, ShareType
from uuid import UUID


router = APIRouter()

# @router.post("/", response_model=ShareType)
# def create_share_type(share_type: ShareTypeCreate, db: Session = Depends(get_db)):
#     return crud.create_share_type(db, share_type)

@router.get("/{share_type_id}", response_model=ShareType)
def get_share_type(share_type_id: int, db: Session = Depends(get_db)):
    share_type = crud.get_share_type(db, share_type_id)
    if not share_type:
        raise HTTPException(status_code=404, detail="ShareType not found")
    return share_type

@router.get("/", response_model=list[ShareType])
def get_all_share_types(db: Session = Depends(get_db)):
    return crud.get_all_share_types(db)
