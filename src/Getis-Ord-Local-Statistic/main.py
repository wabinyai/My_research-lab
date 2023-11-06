from utils import fetch_data_from_api, get_data_for_getis, Getis_Ord_Local_regression, plot_Getis_Ord_local
from datetime import datetime
from datetime import timedelta

# Specify the airqloud_id
airqloud_id = "641b3069572090002992a7a1"

# Usage example:
start_time = datetime(2023, 10, 1, 9, 0, 0)
end_time = datetime(2023, 11, 6, 9, 0, 0)

# Call the function with the desired start and end times
data = fetch_data_from_api(airqloud_id, start_time, end_time)


# Fetch data from the API
#data = fetch_data_from_api(airqloud_id)

if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_getis(data)
    gdf= gdf.dropna(subset='calibratedValue')
    print(gdf.info())
    # Calculate Local Moran's I
    g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90 = Getis_Ord_Local_regression(gdf)


    # Plot the results
    plot_Getis_Ord_local(g_local,  significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90, gdf)
else:
    print("Failed to fetch data from the API.")


 