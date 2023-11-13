import json
from datetime import datetime
import libpysal
import geopandas as gpd
import pandas as pd
import requests
import matplotlib.pyplot as plt
from configure import Config
from pysal.explore import esda
import folium

def fetch_data_from_api(grid_id, start_time, end_time, page  ) -> list:
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
    

def generate_report(data):
    df = pd.DataFrame(data)
    month_under_study = pd.to_datetime(df['time']).dt.month_name().unique()[0]
    mean_pm25 = df['pm2_5']['value'].mean()
    top_locations = df.groupby('siteDetails.formatted_name')['pm2_5']['value'].mean().nlargest(5)
    bottom_locations = df.groupby('siteDetails.formatted_name')['pm2_5']['value'].mean().nsmallest(3)
    trend = "Increasing" if df['pm2_5']['value'].diff().mean() > 0 else "Decreasing"

    if trend == "Increasing":
        health_advice = "Take precautions, as air quality is worsening."
        reasons = "Possible reasons for the increase include industrial activities, wildfires, or vehicular emissions."
    else:
        health_advice = "Good news! Air quality is improving."
        reasons = "Possible reasons for the decrease include reduced industrial activities, improved emissions control, or weather conditions."

    return month_under_study, mean_pm25, top_locations, bottom_locations, trend, health_advice, reasons    