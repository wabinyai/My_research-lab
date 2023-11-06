from utils import fetch_data_from_api, get_data_for_getis, Getis_Ord_Local_regression, plot_Getis_Ord_local

# Specify the airqloud_id
airqloud_id = "653cb91cc0ad670013b28160"

# Fetch data from the API
data = fetch_data_from_api(airqloud_id)

if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_getis(data)

    # Calculate Local Moran's I
    g_local, significant_hot_spots, significant_cold_spots, not_significant = Getis_Ord_Local_regression(gdf)

    # Plot the results
    plot_Getis_Ord_local(g_local, significant_hot_spots, significant_cold_spots, not_significant, gdf)
else:
    print("Failed to fetch data from the API.")


 