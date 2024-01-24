import json
from datetime import datetime
import requests
import pandas as pd
from google.cloud import bigquery, storage
#from pymongo import MongoClient
#from sqlalchemy import create_engine
from google.cloud import bigquery
from google.oauth2 import service_account

from configure import Config

def fetch_air_quality_data(grid_id, start_time, end_time, page  ) -> list:
    # Convert start_time and end_time to ISO format
    start_time_iso = start_time.isoformat() + 'Z'
    end_time_iso = end_time.isoformat() + 'Z'
    
    grid_params = {
        "token": Config.AIRQO_API_TOKEN,
        "startTime": start_time_iso,
        "endTime": end_time_iso,
        "recent": "no",
        "page": page
    }
    
    grid_url = f"https://platform.airqo.net/api/v2/devices/measurements/grids/{grid_id}"
     
    grid_response = requests.get(grid_url, params=grid_params)
    if grid_response.status_code == 200:
        data = grid_response.json()

        # Extracting only the 'site_id' from each measurement
        site_ids = [measurement.get('site_id') for measurement in data.get('measurements', [])]

        return site_ids
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []

# Create a BigQuery client
client = bigquery.Client()
def query_bigquery(site_ids, start_time, end_time):
    # Construct the BigQuery SQL query
    query = f"""
        SELECT site_id, timestamp,site_name,site_latitude,site_longitude,pm2_5,pm2_5_raw_value,pm2_5_calibrated_value,
        pm10,pm10_raw_value,pm10_calibrated_value,country,region,city,county
        FROM `airqo-250220.consolidated_data.hourly_device_measurements`
        WHERE site_id IN UNNEST({site_ids})
        AND timestamp BETWEEN TIMESTAMP('{start_time.isoformat()}')
        AND TIMESTAMP('{end_time.isoformat()}')
        AND NOT pm2_5 IS NULL
    """

    # Execute the query
    query_job = client.query(query)

    # Fetch and return the results
    data = query_job.result()
    return data



 
