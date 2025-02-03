from app.models.payment_status import PaymentStatus  # Renaming the import
from sqlalchemy.orm import Session



# get all payment status
def get_payment_status(db: Session):
    #payment_status_values = db.query(payment_status.PaymentStatus).all()
    payment_status_values = db.query(PaymentStatus).all()
    # give a key value pair where key is the status in lower case and value is the id
    payment_status_values = {status.status.lower(): int(status.id) for status in payment_status_values}
    return payment_status_values

