from utils import fetch_data_from_api, get_data_for_getis, Getis_Ord_Local_regression, plot_Getis_Ord_local
from datetime import datetime
from datetime import timedelta

# Specify the grid_id
grid_id = "64b7b654d7249f0029fecd51"

# Usage example:
start_time = datetime(2023, 10, 1, 9, 0, 0)
end_time = datetime(2023, 11, 20, 9, 0, 0)

data = fetch_data_from_api(grid_id, start_time, end_time)

if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_getis(data)
    
    # Print the columns to check if 'calibratedValue' is present
    print("Columns in GeoDataFrame:", gdf.columns)

    # Check if 'calibratedValue' is present before dropping NaN values
    if 'calibratedValue' in gdf.columns:
        gdf = gdf.dropna(subset=['calibratedValue'])
        print(gdf.info())
        
        # Calculate Local Moran's I
        g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90 = Getis_Ord_Local_regression(gdf)

        plot_Getis_Ord_local(g_local,  significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90, gdf)
    else:
        print("No measurements for this search.")
else:
    print("Failed to fetch data from the API.")

 