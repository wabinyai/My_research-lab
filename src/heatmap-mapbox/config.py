import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

# Add any other configuration variables you need
