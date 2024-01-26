import json
from datetime import datetime
import requests
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from configure import Config

def fetch_air_quality_data(grid_id, start_time, end_time) -> list:
    # Convert start_time and end_time to ISO format
    start_time_iso = start_time.isoformat() + 'Z'
    end_time_iso = end_time.isoformat() + 'Z'

    grid_params = {
        "token": Config.AIRQO_API_TOKEN,
        "startTime": start_time_iso,
        "endTime": end_time_iso,
        "recent": "no"
    }

    grid_url = f"https://platform.airqo.net/api/v2/devices/measurements/grids/{grid_id}"

    try:
        grid_response = requests.get(grid_url, params=grid_params)
        grid_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = grid_response.json()

        # Extracting only the 'site_id' from each measurement
        site_ids = [measurement.get('site_id') for measurement in data.get('measurements', [])]

        return site_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching air quality data: {e}")
        return []

# Create a BigQuery client
client = bigquery.Client()

def query_bigquery(site_ids, start_time, end_time):
    # Construct the BigQuery SQL query
    query = f"""
        SELECT site_id, timestamp, site_name, site_latitude, site_longitude, pm2_5, pm2_5_raw_value,
        pm2_5_calibrated_value, pm10, pm10_raw_value, pm10_calibrated_value, country, region, city, county
        FROM `airqo-250220.consolidated_data.hourly_device_measurements`
        WHERE site_id IN UNNEST({site_ids})
        AND timestamp BETWEEN TIMESTAMP('{start_time.isoformat()}')
        AND TIMESTAMP('{end_time.isoformat()}')
        AND NOT pm2_5 IS NULL
    """

    try:
        # Execute the query
        query_job = client.query(query)

        # Fetch and return the results as a Pandas DataFrame
        data = query_job.to_dataframe()
        return data
    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return None

def results_to_dataframe(results):
    # Convert 'timestamp' to datetime format
    df = pd.DataFrame(results)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create additional columns using dt accessor
    df['date'] = df['timestamp'].dt.date
    df['day'] = df['timestamp'].dt.day_name()
    df['hour'] = df['timestamp'].dt.hour
    df['year'] = df['timestamp'].dt.year

    return df

def calculate_mean_daily_pm2_5(dataframe):
    return dataframe.groupby('timestamp')['pm2_5'].mean()

def calculate_mean_pm2_5_by_site_name(dataframe):
    return dataframe.groupby('site_name')['pm2_5'].mean()
