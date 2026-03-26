import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    BASE_URL = os.getenv("BASE_URL")

settings = Settings()