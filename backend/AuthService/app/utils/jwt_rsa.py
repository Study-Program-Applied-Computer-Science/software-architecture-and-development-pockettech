from datetime import datetime, timedelta
import jwt
from app.config import settings

# Load RSA keys
with open(settings.private_key_path, "rb") as private_file:
    PRIVATE_KEY = private_file.read()

with open(settings.public_key_path, "rb") as public_file:
    PUBLIC_KEY = public_file.read()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
   
    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "1", 
        "jku": "http://localhost:8001/.well-known/jwks.json"  
    }
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256", headers=header)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode the JWT token."""
    print("PUBLIC_KEY")
    payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    print("payload",payload)
    return payload
