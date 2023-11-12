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

def get_data_for_moran(data):
    # Extract relevant data for Local Moran's I
    features = []
    for measurement in data['measurements']:
        pm2_5 = measurement.get('pm2_5', {})
        calibrated_value = pm2_5.get('calibratedValue')
        if calibrated_value is None:
                calibrated_value = pm2_5.get('value')
        latitude = measurement['siteDetails']['approximate_latitude']
        longitude = measurement['siteDetails']['approximate_longitude']
        features.append({'calibratedValue': calibrated_value, 'latitude': latitude, 'longitude': longitude})
        feature = pd.DataFrame(features)
        feature= feature.groupby(['latitude', 'longitude'])['calibratedValue'].mean().reset_index()
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(features, geometry=gpd.points_from_xy([f['longitude'] for f in features], [f['latitude'] for f in features]))
    return gdf  

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

def plot_folium_map(moran_loc, gdf):
    # Create a Folium map
    gdf['cluster_category'] = ['HH' if c == 1 else 'LH' if c == 2 else 'LL' if c == 3 else 'HL' if c == 4 else 'NS' for c in moran_loc.q]
    m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()],  zoom_start=12)

    # Define a smaller radius for the circle markers
    circle_radius = 5  # Adjust this value as needed to reduce the size of the circles

    # Add colored markers to the map based on the cluster category
    for index, row in gdf.iterrows():
        category = row['cluster_category']
        if category == 'HH':
            color = 'red'
        elif category == 'LH':
            color = 'green'
        elif category == 'LL':
            color = 'blue'
        elif category == 'HL':
            color = 'purple'
        else:
            color = 'grey'

        folium.CircleMarker(
            [row['latitude'], row['longitude']],
            radius=circle_radius,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # Create a legend for the colors
    legend_html = """
        <div style="position: fixed;
                    bottom: 50px; left: 50px; width: 120px; height: 130px;
                    border:2px solid grey; z-index:9999; font-size:12px;
                    background-color:white;
                    ">&nbsp;<b> Legend:PM<sub>2.5</sub> </b><br>
                      &nbsp; HH Cluster&nbsp; <i class="fa fa-circle" style="color:red"></i><br>
                      &nbsp; LH Cluster&nbsp; <i class="fa fa-circle" style="color:green"></i><br>
                      &nbsp; LL Cluster&nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
                      &nbsp; HL Cluster&nbsp; <i class="fa fa-circle" style="color:purple"></i><br>
                      &nbsp; Not Significant &nbsp; <i class="fa fa-circle" style="color:grey"></i>
        </div>
    """

    # Create a folium.element.MacroElement with the legend HTML
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the map to an HTML file for viewing
    #m.save('Local_Moran_I_cluster_map.html')  

    # Display the map
    return m
