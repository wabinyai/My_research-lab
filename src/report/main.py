from utils import fetch_air_quality_data, read_air_quality_data, calculate_average_pm2_5_by_site, calculate_monthly_average_pm2_5,month_unique
from datetime import datetime

# Specify the airqloud_id
grid_id = "6542358ddcd81300139b4c1b"
start_time = datetime(2023, 7, 1, 9, 0, 0)
end_time = datetime(2023, 10, 30, 9, 0, 0)
page = 1
top_location = 6
least_location = 1

# Call the function with the desired start and end times
data = fetch_air_quality_data(grid_id, start_time, end_time, page)

# Check if data is not empty before generating the report
if data:
    # Generate the report
    air_quality_data = read_air_quality_data(data)
    avg_pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)

    # Identify the top 5 sites with the highest average PM2.5 values
    top_PM_sites = avg_pm2_5_by_site.nlargest(top_location, "pm2_5_value")  # Adjust column name if needed

    # Identify the least 3 sites with the lowest average PM2.5 values
    least_PM_sites = avg_pm2_5_by_site.nsmallest(least_location, "pm2_5_value")  # Adjust column name if needed

    # Print or use the generated report data as needed
    print(f"Top {top_location} sites with highest average PM2.5 values:")
    print(top_PM_sites)

    print(f"\nLeast {least_location} sites with lowest average PM2.5 values:")
    print(least_PM_sites)

    print(f"\nLeast monthly sites with lowest average PM2.5 values:")
    monthly_avg_pm2_5 = calculate_monthly_average_pm2_5(air_quality_data)
    print(monthly_avg_pm2_5)

    print(f"\nMonths under study:")
    month_unique_place = month_unique(air_quality_data)
    print(month_unique_place)
else:
    print("No data available for the specified time range.")

