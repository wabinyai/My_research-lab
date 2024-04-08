import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)
class Config:
    BIGQUERY_SITES = os.getenv("BIGQUERY_SITES")
    BIGQUERY_AIRQLOUDS_SITES = os.getenv("BIGQUERY_AIRQLOUDS_SITES")
    BIGQUERY_HOURLY_DATA = os.getenv("BIGQUERY_HOURLY_DATA")
    AIRQO_API_TOKEN = os.getenv("AIRQO_API_TOKEN")
    DEVICE_REGISTRY_URL = os.getenv("DEVICE_REGISTRY_URL")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_CREDENTIALS_EMAIL = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_EMAIL")
    BIGQUERY_HOURLY_CONSOLIDATED = os.getenv("BIGQUERY_HOURLY_CONSOLIDATED")
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")
    
    