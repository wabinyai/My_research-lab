import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import request

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)


class Config:
    # APIs
    BASE_URL_V2 = "/api/v2/spatial"
    BASE_URL_V1 = "/api/v1/spatial"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    AIRQO_API_TOKEN = os.getenv("AIRQO_API_TOKEN")


