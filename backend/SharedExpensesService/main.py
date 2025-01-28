from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import (
    shared_group,
    shared_transaction,
    share_type,
    payment_status,
    shared_group_participants,
)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}


@app.on_event("startup")
async def list_routes():
    for route in app.routes:
        print(f"Path: {route.path} | Name: {route.name}")


# Include routers
app.include_router(shared_group.router, prefix="/shared-group", tags=["SharedGroup"])
app.include_router(shared_transaction.router, prefix="/shared-transaction", tags=["SharedTransaction"])
app.include_router(share_type.router, prefix="/share-type", tags=["ShareType"])
app.include_router(payment_status.router, prefix="/payment-status", tags=["PaymentStatus"])
app.include_router(shared_group_participants.router, prefix="/shared-group-participants", tags=["SharedGroupParticipants"])
