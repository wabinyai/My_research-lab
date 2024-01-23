import json
from utils import fetch_air_quality_data, read_air_quality_data, calculate_average_pm2_5_by_site, calculate_monthly_average_pm2_5, month_unique
from datetime import datetime

# Specify the airqloud_id
grid_id = "64b7f325d7249f0029fed743"
start_time = datetime(2023, 1, 1, 9, 0, 0)
end_time = datetime(2024, 1, 22, 9, 0, 0)
page = 1
top_location = 6
least_location = 1

# Call the function with the desired start and end times
data = fetch_air_quality_data(grid_id, start_time, end_time, page)

# Create a dictionary to hold the data
report_data = {}

# Check if data is not empty before generating the report
if data:
    # Generate the report
    air_quality_data = read_air_quality_data(data)
    avg_pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)

    # Identify the top 5 sites with the highest average PM2.5 values
    top_PM_sites = avg_pm2_5_by_site.nlargest(top_location, "pm2_5_value").to_dict(orient='records')  # Convert DataFrame to dictionary

    # Identify the least 3 sites with the lowest average PM2.5 values
    least_PM_sites = avg_pm2_5_by_site.nsmallest(least_location, "pm2_5_value").to_dict(orient='records')  # Convert DataFrame to dictionary

    # Populate the dictionary with the report data
    report_data["Top_sites_with_highest_PM2.5_values"] = top_PM_sites
    report_data["Least_sites_with_lowest_PM2.5_values"] = least_PM_sites

    # Calculate monthly average PM2.5 values
    monthly_avg_pm2_5 = calculate_monthly_average_pm2_5(air_quality_data).to_dict(orient='records')  # Convert DataFrame to dictionary
    report_data["Monthly_avg_PM2.5_values"] = monthly_avg_pm2_5

    # Identify unique months under study
    month_unique_place = month_unique(air_quality_data).tolist()  # Convert unique values to a list
    report_data["Months_under_study"] = month_unique_place
else:
    report_data["No_data_available"] = "No data available for the specified time range."

# Convert the dictionary to a JSON string
json_string = json.dumps(report_data, indent=2)

# Print the JSON string
print(json_string)
