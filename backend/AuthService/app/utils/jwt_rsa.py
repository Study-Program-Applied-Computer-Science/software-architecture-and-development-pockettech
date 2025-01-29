from datetime import datetime, timedelta
import jwt
from app.config import settings

# Load RSA keys
with open(settings.private_key_path, "rb") as private_file:
    PRIVATE_KEY = private_file.read()

with open(settings.public_key_path, "rb") as public_file:
    PUBLIC_KEY = public_file.read()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """Create a JWT token with RSA encryption."""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode the JWT token."""
    payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    return payload
