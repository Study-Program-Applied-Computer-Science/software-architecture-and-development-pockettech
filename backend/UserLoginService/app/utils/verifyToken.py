import os
from urllib import response
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the VERIFY_TOKEN_URL from the environment (AuthService endpoint)
VERIFY_TOKEN_URL = os.getenv("VERIFY_TOKEN_URL")

# Helper function to verify the token via the AuthService API
def verify_token_via_api(authorization: str):
    try:
        print("VERIFY_TOKEN_URL",authorization)
        print("VERIFY_TOKEN_URL",VERIFY_TOKEN_URL)

        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")
    

        try:
            response = requests.get(VERIFY_TOKEN_URL,
             headers={"Authorization": authorization}  
         )
        except requests.exceptions.RequestException as e:
            print("Error: Cannot connect to AuthService", e)
          
        print("response",response)


        # If the response is not 200 OK, raise an HTTPException
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Invalid token")
            )

        # Return the response from AuthService (which should contain user data)
        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error connecting to auth service")
