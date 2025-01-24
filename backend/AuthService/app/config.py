from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


print("Current working directory:", os.getcwd())

# Load environment variables from the .env file
load_dotenv()

# Print the values of the environment variables to debug
print("user_login_service_url:", os.getenv('USER_LOGIN_SERVICE_URL'))
print("private_key_path:", os.getenv('PRIVATE_KEY_PATH'))
print("public_key_path:", os.getenv('PUBLIC_KEY_PATH'))

class Settings(BaseSettings):
    user_login_service_url: str
    private_key_path: str
    public_key_path: str

    class Config:
        env_file = ".env"






settings = Settings()
