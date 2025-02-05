from fastapi import APIRouter
from app.utils.jwt_rsa import load_public_key

import base64

def base64url_encode(data: int) -> str:
    """Encodes an integer into Base64-URL encoding without padding."""
    byte_data = data.to_bytes((data.bit_length() + 7) // 8, byteorder="big")
    return base64.urlsafe_b64encode(byte_data).decode("utf-8").rstrip("=")

router = APIRouter()

@router.get("/.well-known/jwks.json", tags=["Public Key"])
def get_jwks():
    """Endpoint to serve JWKS (JSON Web Key Set)"""
    n, e = load_public_key()
    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "1",  
                "use": "sig", 
                "alg": "RS256",
                "n": base64url_encode(n),  
                "e": base64url_encode(e)  
            }
        ]
    }
    return jwks
