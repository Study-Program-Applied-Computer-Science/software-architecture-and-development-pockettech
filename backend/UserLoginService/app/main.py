from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.userRoute import router as auth_router
from app.db.database import Base, engine
from app.models.country import Country
from app.models.user import User
from app.db.init_db import init_db
import os
from dotenv import load_dotenv

from common.config.correlation import CorrelationIdMiddleware
from common.config.logging import setup_logger

from dotenv import dotenv_values

load_dotenv()

DB_SCHEMA = os.getenv("DB_SCHEMA")


print("Creating tables")
Base.metadata.create_all(bind=engine)

init_db()

print("Country schema:", Country.__table__.schema)
print("User schema:", User.__table__.schema)

from sqlalchemy import inspect
inspector = inspect(engine)

print(" Tables in Database:")
for table in inspector.get_table_names(schema=DB_SCHEMA):
    print(f"  - {table}")

app = FastAPI()

# CORS setup
frontend_origin = ["http://localhost:5173"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SERVICE_NAME  = dotenv_values(".env")["SERVICE_NAME"]
logger = setup_logger(SERVICE_NAME)

# Add Correlation ID Middleware
app.add_middleware(CorrelationIdMiddleware)
# Include routers
app.include_router(auth_router, prefix="/api/v1/user", tags=["register"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Finance Management API"}

