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
    BIGQUERY_HOURLY_PREDICTIONS = os.getenv("BIGQUERY_HOURLY_PREDICTIONS")

    POSTGRES_TABLE = os.getenv("POSTGRES_TABLE")
    POSTGRES_CONNECTION_URL = os.getenv("POSTGRES_CONNECTION_URL")
    POSTGRES_TABLE_IMG = os.getenv("POSTGRES_TABLE_IMG")