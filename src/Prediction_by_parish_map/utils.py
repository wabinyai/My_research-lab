import json
from datetime import datetime

import geopandas as gpd
import pandas as pd
import requests
from configure import Config

def fetch_data_from_api(grid_id, start_time, end_time, page) -> list:
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
        return data
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []

def get_grouped_data_for_pm(data):
    # Extract relevant data for Local Moran's I
    features = []
    for measurement in data['measurements']:
        pm2_5 = measurement.get('pm2_5', {})
        calibrated_value = pm2_5.get('calibratedValue', pm2_5.get('value'))
        if calibrated_value is not None:
            latitude = measurement['siteDetails']['approximate_latitude']
            longitude = measurement['siteDetails']['approximate_longitude']
            site_name = measurement['siteDetails']['name']
            features.append({'calibratedValue': calibrated_value, 'latitude': latitude, 'longitude': longitude, 'site_name': site_name})

    feature_df = pd.DataFrame(features)
    gdf = gpd.GeoDataFrame(feature_df, geometry=gpd.points_from_xy(feature_df['longitude'], feature_df['latitude']))
    return gdf

