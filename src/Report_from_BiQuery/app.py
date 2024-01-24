from flask import Flask, jsonify, request
from utils import fetch_air_quality_data, query_bigquery
from datetime import datetime
import itertools
import json

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def get_air_quality_results():
    # Get data from the request
    request_data = request.get_json()

    # Extract parameters from the request data
    grid_id = request_data.get('grid_id')
    # Convert string to datetime objects
    start_time = datetime.fromisoformat(request_data.get('start_time'))
    end_time = datetime.fromisoformat(request_data.get('end_time'))
    page = request_data.get('page', 1)



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
        'measurements': {
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

    # Convert the response data to a JSON-formatted string without escape characters
    json_result = json.dumps(response_data, indent=2, ensure_ascii=False)

    # Print the JSON-formatted string
    #print(json_result)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
