from sqlalchemy.orm import Session
from app.models.payment_status import PaymentStatus
from app.schemas.payment_status import PaymentStatusCreate
from uuid import UUID


# def create_payment_status(db: Session, payment_status: PaymentStatusCreate):
#     db_payment_status = PaymentStatus(status=payment_status.status)
#     db.add(db_payment_status)
#     db.commit()
#     db.refresh(db_payment_status)
#     return db_payment_status

def get_payment_status(db: Session, payment_status_id: int):
    return db.query(PaymentStatus).filter(PaymentStatus.id == payment_status_id).first()

def get_all_payment_statuses(db: Session):
    return db.query(PaymentStatus).all()
