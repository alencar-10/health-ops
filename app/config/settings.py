from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(".env"))

VIVVER_BASE_URL = os.getenv("VIVVER_BASE_URL")
VIVVER_USERNAME = os.getenv("VIVVER_USERNAME")
VIVVER_PASSWORD = os.getenv("VIVVER_PASSWORD")