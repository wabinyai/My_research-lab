from utils import fetch_data_from_api, get_data_for_getis, Getis_Ord_Local_regression, plot_Getis_Ord_local
from datetime import datetime
from datetime import timedelta

# Specify the airqloud_id
airqloud_id = "61815b91e2dcb4002aad0777"
start_time = datetime(2023, 10, 1, 9, 0, 0)
end_time = datetime(2023, 11, 6, 9, 0, 0)
data = fetch_data_from_api(airqloud_id, start_time, end_time)

if data:
    gdf = get_data_for_getis(data)
    gdf= gdf.dropna(subset='calibratedValue')
    print(gdf.info())
    g_local, significant_hot_spots, significant_cold_spots, not_significant = Getis_Ord_Local_regression(gdf)

    plot_Getis_Ord_local(g_local, significant_hot_spots, significant_cold_spots, not_significant, gdf)
else:
    print("Failed to fetch data from the API.")


 