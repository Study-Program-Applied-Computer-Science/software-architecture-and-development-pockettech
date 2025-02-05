from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    user_login_service_url: str
    private_key_path: str
    public_key_path: str
    service_name: str

    class Config:
        env_file = ".env"


settings = Settings()
