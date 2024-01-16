from utils import fetch_data_from_api, get_data_for_moran, moran_local_regression, plot_moran_local, plot_folium_map
from datetime import datetime
from datetime import timedelta

# Specify the airqloud_id
grid_id = "64b7ba65d7249f0029fecdbd"
start_time = datetime.now() - timedelta(days=14)
end_time = datetime.now()
page = 1

# Call the function with the desired start and end times
data = fetch_data_from_api(grid_id, start_time, end_time, page)

if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_moran(data) 
    # Check if 'calibratedValue' is present before dropping NaN values
    if 'calibratedValue' in gdf.columns:
        print("Number of NaN values in calibratedValue:", gdf['calibratedValue'].isna().sum())
        gdf= gdf.dropna(subset='calibratedValue')
        print(gdf.info())
    # Calculate Local Moran's I
        moran_loc = moran_local_regression(gdf)
        plot_folium_map(moran_loc, gdf)
        print("Local Moran's I save in cluster_map.html")
        plot_moran_local(moran_loc, gdf)      

    else:
         print("No measurements for this search.")
else:
    print("Failed to fetch data from the API.")