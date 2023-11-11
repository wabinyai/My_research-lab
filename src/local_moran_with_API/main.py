from utils import fetch_data_from_api, get_data_for_moran, moran_local_regression, plot_moran_local
from datetime import datetime
from datetime import timedelta

# Specify the airqloud_id
grid_id = "64b7b654d7249f0029fecd51"
start_time = datetime(2023, 10, 5, 9, 0, 0)
end_time = datetime(2023, 11, 5, 9, 0, 0)
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
        plot_moran_local(moran_loc, gdf)

    else:
         print("No measurements for this search.")
else:
    print("Failed to fetch data from the API.")