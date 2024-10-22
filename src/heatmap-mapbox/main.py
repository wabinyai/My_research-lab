import datetime
import cdsapi
import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import zipfile
import json
import os

# Get yesterday's date in YYYY-MM-DD format
yesterday_date = (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')

# Initialize the CDS API client
c = cdsapi.Client()

# Path to the downloaded zip file
zip_file_path = 'download.netcdf_zip'
extract_dir = 'extracted_files'
file_path = 'extracted_files/data.nc'
# Check if the zip file already exists and delete it if so
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
# Check if the file already exists
if not os.path.exists(zip_file_path):
    # Retrieve data from CDS
    c.retrieve(
        'cams-global-atmospheric-composition-forecasts',
        {
            'date': f'{yesterday_date}/{yesterday_date}',  # Set date range to yesterday's date
            'type': 'forecast',
            'format': 'netcdf_zip',
            'leadtime_hour': '12',
            'time': [
                '00:00', '12:00',
            ],
            'variable': [
                'particulate_matter_10um', 'particulate_matter_2.5um',
            ],
        },
        zip_file_path
    )

# Unzipping the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print(f"Files extracted to {extract_dir}")

# Load the NetCDF file
dataset = nc.Dataset(file_path)
print(dataset)

# Extract variables
longitude = dataset.variables['longitude'][:]
latitude = dataset.variables['latitude'][:]
time = dataset.variables['time'][:]
pm25 = dataset.variables['pm2p5'][:]

# Convert longitude from 0-360 to -180 to 180
longitude = np.where(longitude > 180, longitude - 360, longitude)

# Convert time from numerical to datetime
time_units = dataset.variables['time'].units
time = nc.num2date(time, units=time_units)

# Create an xarray Dataset
eaqi_global = xr.Dataset(
    {
        "pm25": (["time", "latitude", "longitude"], pm25)
    },
    coords={
        "longitude": longitude,
        "latitude": latitude,
        "time": time
    }
)

# Define PM2.5 limits globally (can adjust these values if necessary)
pm25_limits = [0, 20, 40, 50, 100, 150, 1200]

# Resample to daily maximum values
eaqi_global_daily = eaqi_global.resample(time='1D').max()

# Squeeze the dataset to drop single-dimensional entries
eaqi_global_daily = eaqi_global_daily.squeeze(drop=True)

# Multiply pm25 by 1,000,000 (1e6)
eaqi_global_daily["pm25"] *= 1e9

# Classify the PM2.5 data globally
pm25_classified = xr.apply_ufunc(np.digitize, eaqi_global_daily["pm25"], pm25_limits)
pm25_classified.name = "classified_pm25"

# Merge the classified array into the original dataset
eaqi_global_daily = eaqi_global_daily.assign({"classified_pm25": pm25_classified})
print(eaqi_global_daily.head())
# Reduce dimensions: take the maximum along the time dimension
final_index = eaqi_global_daily["classified_pm25"].max(dim='time')

# Flatten the data for exporting to JSON
lons, lats = np.meshgrid(eaqi_global_daily.longitude, eaqi_global_daily.latitude)
data_flat = final_index.values.flatten()
lon_flat = lons.flatten()
lat_flat = lats.flatten()


# Create a DataFrame
df = pd.DataFrame({
    'longitude': lon_flat,
    'latitude': lat_flat,
    'pm25_level': data_flat
})

# Export data to JSON
data = {
    "longitude": df['longitude'].tolist(),
    "latitude": df['latitude'].tolist(),
    "pm25_level": df['pm25_level'].tolist()
}

# Check if the JSON file already exists and delete it if so
json_file_path = 'aqi_data.json'
if os.path.exists(json_file_path):
    os.remove(json_file_path)

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file)
