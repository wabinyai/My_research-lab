import os
from dotenv import load_dotenv

load_dotenv()

# Read environment variables
BIGQUERY_CONSOLIDATED_DATA = os.getenv("BIGQUERY_CONSOLIDATED_DATA")
