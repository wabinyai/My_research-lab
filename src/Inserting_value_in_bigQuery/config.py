import os

import urllib3
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    MEASUREMENTS_TOPIC = os.getenv('MEASUREMENTS_TOPIC')
    AIRQLOUDS_TOPIC = os.getenv('AIRQLOUDS_TOPIC')
    BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')
    GP_MODEL_DB = os.getenv('GP_MODEL_DB')
    GP_MODEL_DB_URI = os.getenv('GP_MODEL_DB_URI')

    BIGQUERY_MEASUREMENTS_PREDICTIONS = os.getenv('BIGQUERY_MEASUREMENTS_PREDICTIONS')
    BIGQUERY_SITES = os.getenv("BIGQUERY_SITES")
    BIGQUERY_AIRQLOUDS_SITES = os.getenv("BIGQUERY_AIRQLOUDS_SITES")
    BIGQUERY_HOURLY_DATA = os.getenv("BIGQUERY_HOURLY_DATA")
    BIGQUERY_DEVICE_MEASUREMENT_STAGE = os.getenv("BIGQUERY_DEVICE_MEASUREMENT_STAGE")
    BIGQUERY_DEVICE_MEASUREMENT_PROD = os.getenv("BIGQUERY_DEVICE_MEASUREMENT_PROD")