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

def fetch_data_from_api(grid_id, start_time, end_time) -> list:
    # Convert start_time and end_time to ISO format
    start_time_iso = start_time.isoformat() + 'Z'
    end_time_iso = end_time.isoformat() + 'Z'
    grid_params = {
        "token": Config.AIRQO_API_TOKEN,
        "startTime": start_time_iso,
        "endTime": end_time_iso,
        "recent": "no",
        "page": "1"
    }
    
    grid_url = f"https://platform.airqo.net/api/v2/devices/measurements/grids/{grid_id}"     
    grid_response = requests.get(grid_url, params=grid_params)
    if grid_response.status_code == 200:
        data = grid_response.json()
        return data
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []

def get_data_for_getis(data):
    features = []
    for measurement in data['measurements']:
        pm2_5 = measurement.get('pm2_5', {})
        calibrated_value = pm2_5.get('calibratedValue')
            # Check if calibrated_value is null, if so, use the 'value' instead
        if calibrated_value is None:
             calibrated_value = pm2_5.get('value')
    
        latitude = measurement['siteDetails']['approximate_latitude']
        longitude = measurement['siteDetails']['approximate_longitude']
        features.append({'calibratedValue': calibrated_value, 'latitude': latitude, 'longitude': longitude})
        feature = pd.DataFrame(features)
        feature= feature.groupby(['latitude', 'longitude'])['calibratedValue'].mean().reset_index()
    
    gdf = gpd.GeoDataFrame(features, geometry=gpd.points_from_xy([f['longitude'] for f in features], [f['latitude'] for f in features]))
    return gdf  # Return the GeoDataFrame


def Getis_Ord_Local_regression(gdf):
    w = KNN.from_dataframe(gdf, k=7) 
    pm2_5 = gdf['calibratedValue'] 
    g_local = G_Local(pm2_5, w)
    p_values = g_local.p_sim
    z_scores = g_local.Zs
        # Significance levels for clusters
    alpha_99 = 0.01  # 99% confidence level
    alpha_95 = 0.05  # 95% confidence level
    alpha_90 = 0.10  # 90% confidence level
    significant_hot_spots_99 = (p_values < alpha_99) & (z_scores > 0)
    significant_hot_spots_95 = (p_values < alpha_95) & (z_scores > 0)
    significant_hot_spots_90 = (p_values < alpha_90) & (z_scores > 0)

    significant_cold_spots_99 = (p_values < alpha_99) & (z_scores < 0)
    significant_cold_spots_95 = (p_values < alpha_95) & (z_scores < 0)
    significant_cold_spots_90 = (p_values < alpha_90) & (z_scores < 0)
    
    return g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90
 
def plot_Getis_Ord_local(g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90, gdf):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot the GeoDataFrame with different colors and marker sizes for significant hot spots
    gdf[significant_hot_spots_99].plot(ax=ax, markersize=40, color='red', alpha=0.9, label='Hot Spot (99%)')
    gdf[significant_hot_spots_95].plot(ax=ax, markersize=30, color='#FFAC1C', alpha=0.9, label='Hot Spot (95%)')
    gdf[significant_hot_spots_90].plot(ax=ax, markersize=20, color='yellow', alpha=0.9, label='Hot Spot (90%)')
    
    # Plot the GeoDataFrame with different colors and marker sizes for significant cold spots
    gdf[significant_cold_spots_99].plot(ax=ax, markersize=40, color='blue', alpha=0.9, label='Cold Spot (99%)')
    gdf[significant_cold_spots_95].plot(ax=ax, markersize=30, color='lightblue', alpha=0.9, label='Cold Spot (95%)')
    gdf[significant_cold_spots_90].plot(ax=ax, markersize=20, color='green', alpha=0.9, label='Cold Spot (90%)')
    
    # Plot non-significant areas with gray markers
    gdf[~(significant_hot_spots_99 | significant_hot_spots_95 | significant_hot_spots_90 | significant_cold_spots_99 | significant_cold_spots_95 | significant_cold_spots_90)].plot(ax=ax, markersize=20, color='gray', alpha=0.7, label='Not Significant')
    
    plt.title("Getis-Ord Local Statistic - Hot Spots, Cold Spots, and Not Significant")
    plt.legend()
    plt.show()
