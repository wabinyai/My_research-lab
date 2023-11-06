from utils import fetch_data_from_api, get_data_for_moran, moran_local_regression, plot_moran_local

# Specify the airqloud_id
airqloud_id = "618b850c9326560036a453eb"

# Fetch data from the API
data = fetch_data_from_api(airqloud_id)

if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_moran(data)

    # Calculate Local Moran's I
    moran_loc = moran_local_regression(gdf)

    # Plot the results
    plot_moran_local(moran_loc, gdf)
else:
    print("Failed to fetch data from the API.")
