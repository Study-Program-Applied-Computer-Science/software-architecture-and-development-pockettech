from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.authRoute import router as auth_router
from app.config import settings
import uvicorn

app = FastAPI()

# CORS setup
origins = ["http://localhost:3000"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
print("auth service port--------------------------------------------")

@app.get("/")
def root():
    return {"message": "AuthService is up and running!"}

print("auth service port--------------------------------------------")

# add port to run the service

for route in app.routes:
    print(route)
