from datetime import datetime, timedelta
import jwt
from app.config import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# Load RSA keys
with open(settings.private_key_path, "rb") as private_file:
    PRIVATE_KEY = private_file.read()

with open(settings.public_key_path, "rb") as public_file:
    PUBLIC_KEY = public_file.read()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=10)):
   
    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "1", 
        "jku": "http://auth_service:8001/.well-known/jwks.json"  
    }
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256", headers=header)
    return encoded_jwt


# Function to load public key and extract modulus and exponent
def load_public_key():
    # Load the public key from the PEM format
    public_key = serialization.load_pem_public_key(PUBLIC_KEY)
    if isinstance(public_key, rsa.RSAPublicKey):
        # Extract the modulus (n) and exponent (e)
        n = public_key.public_numbers().n
        e = public_key.public_numbers().e
        print("Public key loaded successfully.",n,"-----e----",e)
        return n, e
    raise ValueError("The public key is not of type RSA.")

# Call this function to extract modulus and exponent
PUBLIC_KEY_N, PUBLIC_KEY_E = load_public_key()