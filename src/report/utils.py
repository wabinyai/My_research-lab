from datetime import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
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

        time_str = measurement.get("time")
        frequency = measurement.get("frequency")

                # Extracting date, year, day, and month from the time field
        time_dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        date = time_dt.date()
        hour = time_dt.hour
        year = time_dt.year
        day = time_dt.day
        month = time_dt.month
        
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
            "time": time_str,
            "date": date,
            "hour": hour,
            "year": year,
            "day": day,
            "month": month,
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
        "pm10_value": "mean",
        "latitude": "first",   # Assuming latitude is constant for a site
        "longitude": "first",   # Assuming longitude is constant for a site
    }).reset_index()  # Resetting the index

    # Round specified columns to two decimal placess
    avg_pm2_5_by_site[["pm2_5_value","pm10_value",  "latitude", "longitude"]] = avg_pm2_5_by_site[["pm2_5_value", "pm10_value","latitude", "longitude"]].round(2)

    return avg_pm2_5_by_site

def calculate_monthly_average_pm2_5(data):
    df = pd.DataFrame(data)
    df = df.dropna()
    month_average = df.groupby("month").agg({
        "pm2_5_value": "mean",
        "pm10_value": "mean"
    }).reset_index()  # Resetting the index
    # Sort by month in ascending order
    month_average = month_average.sort_values(by="month")

    return month_average

def calculate_date_average_pm2_5(data):
    df = pd.DataFrame(data)
    df = df.dropna()
    date_average = df.groupby("date").agg({
        "pm2_5_value": "mean",
        "pm10_value": "mean"
    }).reset_index()  # Resetting the index
    # Sort by month in ascending order
    date_average = date_average.sort_values(by="date")

    return date_average

def calculate_yearly_average_pm2_5(data):
    df = pd.DataFrame(data)
    df = df.dropna()
    yearly_average = df.groupby("year").agg({
        "pm2_5_value": "mean",
        "pm10_value": "mean"
    }).reset_index()  # Resetting the index
    # Sort by month in ascending order
    yearly_average = yearly_average.sort_values(by="year")

    return yearly_average

def calculate_diurnal_average_pm2_5(data):
    df = pd.DataFrame(data)
    df = df.dropna()
    diurnal_average = df.groupby("hour").agg({
        "pm2_5_value": "mean",
        "pm10_value": "mean"
    }).reset_index()  # Resetting the index
    # Sort by month in ascending order
    diurnal_average = diurnal_average.sort_values(by="hour")

    return diurnal_average

def month_unique(data):
    df = pd.DataFrame(data)
    df = df.dropna()
    monthly_unique = df.month.nunique()

    return monthly_unique