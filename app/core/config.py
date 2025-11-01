import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app/database/database.db")

settings = Settings()
