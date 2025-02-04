import jwt
import requests
from fastapi import HTTPException
from jwt import PyJWKClient

def verify_token_via_jku(token: str):
    try:
        print("token",token)
        # Decode token headers to get JKU (JSON Key URL)
        headers = jwt.get_unverified_header(token)
        print("headers",headers)
        jku_url = headers.get("jku")
        print("jku_url",jku_url)
        if not jku_url:
            raise HTTPException(status_code=401, detail="JKU not found in token")
        
        # Fetch the public key from JKU
        jwk_client = PyJWKClient(jku_url)
        print("jwk_client",jwk_client)
        try:
            signing_key = jwk_client.get_signing_key_from_jwt(token)
            print("signing_key",signing_key)
        except Exception as e:
            print("Error fetching public key from JKU", e)
        
        # Decode token with the fetched public key
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=[headers.get("alg", "RS256")],
            options={"verify_aud": False}  
        )
        print("payload",payload)
        
        # Extract roles and user_id
        id = payload.get("id")
        roles = payload.get("roles", [])
        if not id or not roles:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        return {"id": id, "roles": roles}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except requests.RequestException:
        raise HTTPException(status_code=401, detail="Error fetching public key from JKU")
    
def verify_roles(token: str, allowed_roles: list[str]):
    try:
        token_data = verify_token_via_jku(token)
        user_roles = token_data.get("roles", [])
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    