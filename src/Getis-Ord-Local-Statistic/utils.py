import json
from datetime import datetime
import libpysal
import geopandas as gpd
import pandas as pd
import requests
import matplotlib.pyplot as plt
from configure import Config
from libpysal.weights import KNN
from esda import G_Local


 



def fetch_data_from_api(airqloud_id, start_time, end_time) -> list:
    # Convert start_time and end_time to ISO format
    start_time_iso = start_time.isoformat() + 'Z'
    end_time_iso = end_time.isoformat() + 'Z'
    
     
    airqloud_params = {
        "token": Config.AIRQO_API_TOKEN,
        "startTime": start_time_iso,
        "endTime": end_time_iso,
        "recent": "no",
        "page": "2"
    }
    
    airqloud_url = f"https://platform.airqo.net/api/v2/devices/measurements/airqlouds/{airqloud_id}"
     
    airqloud_response = requests.get(airqloud_url, params=airqloud_params)
    if airqloud_response.status_code == 200:
        data = airqloud_response.json()
        return data
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []

def get_data_for_getis(data):

    features = []
    for measurement in data['measurements']:
        pm2_5 = measurement.get('pm2_5', {})
        calibrated_value = pm2_5.get('calibratedValue')
        latitude = measurement['siteDetails']['approximate_latitude']
        longitude = measurement['siteDetails']['approximate_longitude']
        features.append({'calibratedValue': calibrated_value, 'latitude': latitude, 'longitude': longitude})

    
    gdf = gpd.GeoDataFrame(features, geometry=gpd.points_from_xy([f['longitude'] for f in features], [f['latitude'] for f in features]))
    return gdf  # Return the GeoDataFrame


def Getis_Ord_Local_regression(gdf):
    w = KNN.from_dataframe(gdf, k=7) 
    pm2_5 = gdf['calibratedValue'] 
    g_local = G_Local(pm2_5, w)
    p_values = g_local.p_sim
    z_scores = g_local.Zs
    alpha = 0.05
    significant_hot_spots = (p_values < alpha) & (z_scores > 0)
    significant_cold_spots = (p_values < alpha) & (z_scores < 0)
    not_significant = p_values >= alpha
    
    return g_local, significant_hot_spots, significant_cold_spots, not_significant
 


def plot_Getis_Ord_local(g_local, significant_hot_spots, significant_cold_spots, not_significant, gdf):
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, markersize=20, color='gray', alpha=0.7, label='Not Significant')
    gdf[significant_hot_spots].plot(ax=ax, markersize=40, color='red', alpha=0.7, label='Hot Spot')
    gdf[significant_cold_spots].plot(ax=ax, markersize=40, color='blue', alpha=0.7, label='Cold Spot')
    plt.title("Getis-Ord Local Statistic - Hot Spots, Cold Spots, and Not Significant")
    plt.legend()
    plt.show()