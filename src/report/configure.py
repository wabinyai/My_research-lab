import os
from dotenv import load_dotenv

load_dotenv()

# Set the environment variable for GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_application_credentials.json"
BIGQUERY_CONSOLIDATED_DATA = os.getenv("BIGQUERY_CONSOLIDATED_DATA")
