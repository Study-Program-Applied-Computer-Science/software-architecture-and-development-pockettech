import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
    ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

settings = Settings()