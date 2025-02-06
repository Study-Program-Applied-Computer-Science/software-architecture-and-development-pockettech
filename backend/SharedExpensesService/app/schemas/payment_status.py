from pydantic import BaseModel

class PaymentStatusBase(BaseModel):
    status: str

class PaymentStatusCreate(PaymentStatusBase):
    pass

class PaymentStatus(PaymentStatusBase):
    id: int

    class Config:
        orm_mode = True
