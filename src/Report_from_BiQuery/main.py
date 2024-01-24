from utils import fetch_air_quality_data, query_bigquery
from datetime import datetime
import itertools
import json

# Specify the airqloud_id
grid_id = "64b7f325d7249f0029fed743"
start_time = datetime(2024, 1, 2, 9, 0, 0)
end_time = datetime(2024, 1, 19, 12, 0, 0)
page = 1

# Fetch air quality data
site_ids = fetch_air_quality_data(grid_id, start_time, end_time, page)


# Query BigQuery with the retrieved site_ids
bigquery_results = query_bigquery(site_ids, start_time, end_time)

# Convert BigQuery results to a list of dictionaries
result_list = []
for row in itertools.islice(bigquery_results, 15):
    # Convert datetime objects to strings
    row_dict = {key: str(value) if isinstance(value, datetime) else value for key, value in row.items()}
    result_list.append(row_dict)

# Create response data dictionary
response_data = {
    'measurements':{
    'status': 'success',
    'meta': {
        'grid_id': grid_id,
        'period': {
            'startTime': start_time.isoformat(),
            'endTime': end_time.isoformat(),
        },
        'value': result_list,
    }
}
}

# Convert the response data to a JSON-formatted string
json_result = json.dumps(response_data, indent=2)

# Print the JSON-formatted string
print(json_result)
