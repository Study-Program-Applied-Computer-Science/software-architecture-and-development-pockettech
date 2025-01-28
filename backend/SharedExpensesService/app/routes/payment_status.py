from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import payment_status as crud
from app.schemas.payment_status import PaymentStatusCreate, PaymentStatus
from uuid import UUID


router = APIRouter()

# @router.post("/", response_model=PaymentStatus)
# def create_payment_status(payment_status: PaymentStatusCreate, db: Session = Depends(get_db)):
#     return crud.create_payment_status(db, payment_status)

@router.get("/{payment_status_id}", response_model=PaymentStatus)
def get_payment_status(payment_status_id: int, db: Session = Depends(get_db)):
    payment_status = crud.get_payment_status(db, payment_status_id)
    if not payment_status:
        raise HTTPException(status_code=404, detail="PaymentStatus not found")
    return payment_status

@router.get("/", response_model=list[PaymentStatus])
def get_all_payment_statuses(db: Session = Depends(get_db)):
    return crud.get_all_payment_statuses(db)
