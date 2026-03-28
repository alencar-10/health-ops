from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(".env"))

BASE_URL = os.getenv("VIVVER_BASE_URL")  # ← lê VIVVER_BASE_URL do .env
USERNAME = os.getenv("VIVVER_USERNAME")
PASSWORD = os.getenv("VIVVER_PASSWORD")