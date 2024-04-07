import json
from datetime import datetime
import requests
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from configure import Config

from timezonefinder import TimezoneFinder
import pytz

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
                # Convert timestamp to local time based on latitude and longitude
        data['timestamp'] = convert_utc_to_local(data['timestamp'], data['site_latitude'], data['site_longitude'])

        return data
    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return None
    
def convert_utc_to_local(timestamps,site_latitude, site_longitude):
    tf = TimezoneFinder()
    local_times = []

    for timestamp, latitude, longitude in zip(timestamps, site_latitude, site_longitude):
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        timezone = pytz.timezone(timezone_str)
        local_time = timestamp.astimezone(timezone)
        local_times.append(local_time)

    return local_times

def results_to_dataframe(results):
    # Convert 'timestamp' to datetime format
    df = pd.DataFrame(results)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Create additional columns using dt accessor
    df['dates'] = df['timestamp'].dt.date.astype(str)
    df['date'] = pd.to_datetime(df['dates'])
    df['day'] = df['timestamp'].dt.day_name()
    df['hour'] = df['timestamp'].dt.hour
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['month_name'] = df['timestamp'].dt.month_name()   
    df=df.dropna(subset='site_latitude')

    return df
# Define the list of columns as a constant
PM_COLUMNS = ['pm2_5_raw_value', 'pm2_5_calibrated_value', 'pm10_raw_value', 'pm10_calibrated_value']
PM_COLUMNS_CORD = ['pm2_5_raw_value','pm2_5_calibrated_value','pm10_raw_value','pm10_calibrated_value','site_latitude', 'site_longitude']
   
def datetime_pm2_5(dataframe):
    return dataframe.groupby('timestamp')[PM_COLUMNS].mean().reset_index()

def mean_daily_pm2_5(dataframe):
    return dataframe.groupby('date')[PM_COLUMNS].mean().reset_index()

def mean_pm2_5_by_site_name(dataframe):
    pm_result = dataframe.groupby('site_name')[PM_COLUMNS].mean().reset_index()
    result_sorted = pm_result.sort_values(by='pm2_5_calibrated_value', ascending=False)
    return result_sorted


 
def monthly_mean_pm_site_name(dataframe):
    return dataframe.groupby(['site_name','month','year'])[PM_COLUMNS_CORD].mean().reset_index() 

def mean_pm2_5_by_hour(dataframe):
    return dataframe.groupby('hour')[PM_COLUMNS].mean().reset_index()

def mean_pm2_5_by_month_year(dataframe):
    return dataframe.groupby(['month','year'])[PM_COLUMNS].mean().reset_index()

def mean_pm2_5_by_month(dataframe):
    return dataframe.groupby('month')[PM_COLUMNS].mean().reset_index()

def mean_pm2_5_by_month_name(dataframe):
    return dataframe.groupby(['month_name'])[PM_COLUMNS].mean().reset_index()
    
def mean_pm2_5_by_year(dataframe):
    return dataframe.groupby('year')[PM_COLUMNS].mean().reset_index()

def pm_by_city(dataframe):
    return dataframe.groupby(['city','month','year'])[PM_COLUMNS].mean().reset_index()

def pm_by_country(dataframe):
    return dataframe.groupby('country')[PM_COLUMNS].mean().reset_index()

def pm_by_region(dataframe):
    return dataframe.groupby('region')[PM_COLUMNS].mean().reset_index()

 
 