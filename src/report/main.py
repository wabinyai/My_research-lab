# main.py
from utils import fetch_air_quality_data,  read_air_quality_data, calculate_average_pm2_5_by_site
from datetime import datetime

# Specify the airqloud_id
grid_id = "64b7ba65d7249f0029fecdbd"
start_time = datetime(2023, 10, 5, 9, 0, 0)
end_time = datetime(2023, 11, 5, 9, 0, 0)
page = 1

# Call the function with the desired start and end times
data = fetch_air_quality_data(grid_id, start_time, end_time, page)

# Check if data is not empty before generating the report
if data:
    # Generate the report
    air_quality_data = read_air_quality_data(data)
    avg_pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)

    # Identify the top 5 sites with the highest average PM2.5 values
    top_5_sites = avg_pm2_5_by_site.nlargest(5)

    # Identify the least 3 sites with the lowest average PM2.5 values
    least_3_sites = avg_pm2_5_by_site.nsmallest(3)

    # Print or use the generated report data as needed
    print("Top 5 sites with highest average PM2.5 values:")
    print(top_5_sites)

    print("\nLeast 3 sites with lowest average PM2.5 values:")
    print(least_3_sites)

else:
    print("No data available for the specified time range.")
