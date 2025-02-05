from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.authRoute import router as auth_router
from app.config import settings
from app.routes.publicKeyRoute import router as public_key_router
from common.config.correlation import CorrelationIdMiddleware
from common.config.logging import setup_logger

app = FastAPI()

# CORS setup
origins = ["http://localhost:5173"]  # Update as per frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICE_NAME = settings.service_name
logger = setup_logger(SERVICE_NAME)

# Add Correlation ID Middleware
app.add_middleware(CorrelationIdMiddleware)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(public_key_router)

@app.get("/")
def root():
    return {"message": "AuthService is up and running!"}

for route in app.routes:
    print(route)
    print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
