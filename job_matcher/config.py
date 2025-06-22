import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "job_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "remotive_jobs")

# Models
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")