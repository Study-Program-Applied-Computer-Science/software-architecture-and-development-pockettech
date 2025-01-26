from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.userLoginRoute import router as auth_router
from app.db.database import Base, engine
from app.models.country import Country
from app.models.user import User



# Create 'country' first as 'users' has a foreign key reference to it
Country.__table__.create(bind=engine, checkfirst=True)  
User.__table__.create(bind=engine, checkfirst=True)


app = FastAPI()

# CORS setup
frontend_origin = ["http://localhost:3000"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/user", tags=["register"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Finance Management API"}

