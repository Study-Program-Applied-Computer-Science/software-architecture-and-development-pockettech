from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.authRoute import router as auth_router
from app.config import settings
from app.routes.publicKeyRoute import router as public_key_router



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

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(public_key_router)

@app.get("/")
def root():
    return {"message": "AuthService is up and running!"}

for route in app.routes:
    print(route)
    print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
