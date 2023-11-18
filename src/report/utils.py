from datetime import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
from configure import Config
import seaborn as sns
 

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
        return data
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []


def read_air_quality_data(data):
    measurements = data.get("measurements", [])

    result = []
    for measurement in measurements:
        device = measurement.get("device")
        device_id = measurement.get("device_id")
        site_id = measurement.get("site_id")
        time = measurement.get("time")
        frequency = measurement.get("frequency")
        
        pm2_5_value = measurement.get("pm2_5", {}).get("value")
        pm10_value = measurement.get("pm10", {}).get("value")

        site_details = measurement.get("siteDetails", {})
        site_name = site_details.get("formatted_name")
        district = site_details.get("district")
        county = site_details.get("county")
        region = site_details.get("region")
        country = site_details.get("country")

        latitude = site_details.get("approximate_latitude")
        longitude = site_details.get("approximate_longitude")

        result.append({
            "time": time,
            "frequency": frequency,
            "device": device,
            "device_id": device_id,
            "site_id": site_id,
            "pm2_5_value": pm2_5_value,
            "pm10_value": pm10_value,
            "site_name": site_name,
            "latitude": latitude,
            "longitude": longitude,
            "district": district,
            "county": county,
            "region": region,
            "country": country
        })

    return result

 

def calculate_average_pm2_5_by_site(data):
    df = pd.DataFrame(data)
    avg_pm2_5_by_site = df.groupby("site_name").agg({
        "pm2_5_value": "mean",
        "latitude": "first",   # Assuming latitude is constant for a site
        "longitude": "first"   # Assuming longitude is constant for a site
    }).reset_index()  # Resetting the index

    # Round specified columns to two decimal places
    avg_pm2_5_by_site[["pm2_5_value", "latitude", "longitude"]] = avg_pm2_5_by_site[["pm2_5_value", "latitude", "longitude"]].round(2)

    return avg_pm2_5_by_site