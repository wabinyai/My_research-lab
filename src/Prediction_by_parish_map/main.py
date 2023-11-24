from utils import fetch_data_from_api, get_grouped_data_for_pm
import folium
import branca.colormap as cm
from datetime import datetime

def generate_map(grid_id, start_time, end_time):
    # Fetch data from the AirQo API
    df_u22 = fetch_data_from_api(grid_id, start_time, end_time, page=1)
    #print(df_u22)
    # Your existing map creation logic
    df_u2 = get_grouped_data_for_pm(df_u22)
    print(df_u2)

    # Create a folium map centered around the first data point
    map = folium.Map(location=[df_u2['latitude'].iloc[0], df_u2['longitude'].iloc[0]], zoom_start=12)
    # Define a colormap for air quality data
    linear = cm.StepColormap(["#44e527", "#f8fe39", "#ee8327", "#fe0023"],
                           vmin=0, vmax=150, index=[0, 12, 35, 55, 150])
    # Add air quality data markers to the map
    for _, row in df_u2.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            popup=f"Calibrated Value: {round(row['calibratedValue'], 2)}",
                            radius=10,
                            color=linear(row.calibratedValue),  # Change this to your color logic
                            fill=True,
                            fill_color=linear(row.calibratedValue),  # Change this to your color logic
                            opacity=0.7,
                            fill_opacity=0.8
                            ).add_to(map)

    # Save the map as an HTML file
    map.save('map.html')
    
if __name__ == '__main__':
    # Provide the necessary parameters
    grid_id = "6542358ddcd81300139b4c1b"
    start_time = datetime.strptime("2023-10-01T00:00", '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime("2023-11-02T00:00", '%Y-%m-%dT%H:%M')

    # Generate the map
    generate_map(grid_id, start_time, end_time)
