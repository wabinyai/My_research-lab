import json
from datetime import datetime
import libpysal
import geopandas as gpd
import pandas as pd
import requests
import matplotlib.pyplot as plt
from configure import Config
from pysal.explore import esda

def fetch_data_from_api(airqloud_id, start_time, end_time, page  ) -> list:
    # Convert start_time and end_time to ISO format
    start_time_iso = start_time.isoformat() + 'Z'
    end_time_iso = end_time.isoformat() + 'Z'
    
    airqloud_params = {
        "token": Config.AIRQO_API_TOKEN,
        "startTime": start_time_iso,
        "endTime": end_time_iso,
        "recent": "no",
        "page": page
    }
    
    airqloud_url = f"https://platform.airqo.net/api/v2/devices/measurements/airqlouds/{airqloud_id}"
     
    airqloud_response = requests.get(airqloud_url, params=airqloud_params)
    if airqloud_response.status_code == 200:
        data = airqloud_response.json()
        return data
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []

def get_data_for_moran(data):
    # Extract relevant data for Local Moran's I
    features = []
    for measurement in data['measurements']:
        pm2_5 = measurement.get('pm2_5', {})
        calibrated_value = pm2_5.get('calibratedValue')
        latitude = measurement['siteDetails']['approximate_latitude']
        longitude = measurement['siteDetails']['approximate_longitude']
        features.append({'calibratedValue': calibrated_value, 'latitude': latitude, 'longitude': longitude})

        feature = pd.DataFrame(features)
        feature= feature.groupby(['latitude', 'longitude'])['calibratedValue'].mean().reset_index()
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(features, geometry=gpd.points_from_xy([f['longitude'] for f in features], [f['latitude'] for f in features]))
    return gdf  # Return the GeoDataFrame

def moran_local_regression(gdf):
    w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=100, binary=True)
    moran_loc = esda.Moran_Local(gdf['calibratedValue'], w)  # Corrected the column name
    return moran_loc

def plot_moran_local(moran_loc, gdf):
    # Create a new category column based on cluster types
    gdf['cluster_category'] = ['HH' if c == 1 else 'LH' if c == 2 else 'LL' if c == 3 else 'HL' if c == 4 else 'NS' for c in moran_loc.q]
    f, ax = plt.subplots(1, figsize=(10, 10))
    gdf.plot(column='cluster_category', categorical=True, k=5, cmap='viridis', linewidth=0.1, ax=ax, edgecolor='grey', legend=True)
    plt.title("Local Moran's I Cluster Map for PM2.5")
    plt.show()

