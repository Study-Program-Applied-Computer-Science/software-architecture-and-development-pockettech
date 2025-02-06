from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_schema: str
    db_user: str
    db_password: str
    private_key_path: str
    public_key_path: str
    service_name: str

    class Config:
        env_file = ".env"


settings = Settings()
