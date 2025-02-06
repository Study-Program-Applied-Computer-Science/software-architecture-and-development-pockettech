from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.payment_status import PaymentStatus

def init_db():
    # Insert default payment status data if the table is empty
    with SessionLocal() as db:
        if not db.query(PaymentStatus).first():
            # Add default payment statuses
            statuses = [
                PaymentStatus(status="Pending"),
                PaymentStatus(status="Paid"),
                PaymentStatus(status="Failed")
            ]
            db.add_all(statuses)
            db.commit()
            print("Inserted default payment status data.")
