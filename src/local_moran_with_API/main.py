from utils import fetch_data_from_api, get_data_for_moran, moran_local_regression, plot_moran_local
from datetime import datetime
from datetime import timedelta

# Specify the airqloud_id
airqloud_id = "61815b91e2dcb4002aad0777"

# Usage example:
start_time = datetime(2023, 10, 5, 9, 0, 0)
end_time = datetime(2023, 11, 5, 9, 0, 0)

# Call the function with the desired start and end times
data = fetch_data_from_api(airqloud_id, start_time, end_time)



if data:
    # Get the GeoDataFrame with relevant data
    gdf = get_data_for_moran(data)
    gdf= gdf.dropna(subset='calibratedValue')
    print(gdf.info())

    # Calculate Local Moran's I
    moran_loc = moran_local_regression(gdf)

    # Plot the results
    plot_moran_local(moran_loc, gdf)
else:
    print("Failed to fetch data from the API.")
