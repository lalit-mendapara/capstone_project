# Centralizes configuration using environment variables for security.

import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL = os.getenv("MODEL_NAME")
    DB_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    QDRANT_URL = os.getenv("QDRANT_URL")
    PROJECT_NAME = os.getenv("PROJECT_NAME")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

settings= Settings()