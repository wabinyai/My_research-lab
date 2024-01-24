from flask import Flask, jsonify, request
from utils import fetch_air_quality_data, query_bigquery
from datetime import datetime
import itertools

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def get_air_quality_results():
    # Get parameters from the JSON request
    request_data = request.get_json()
    grid_id = request_data.get('grid_id')
    start_time = datetime.strptime(request_data.get('start_time'), '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(request_data.get('end_time'), '%Y-%m-%d %H:%M:%S')
    page = request_data.get('page', 1)

    # Fetch air quality data
    site_ids = fetch_air_quality_data(grid_id, start_time, end_time, page)

    # Query BigQuery with the retrieved site_ids
    bigquery_results = query_bigquery(site_ids, start_time, end_time)

    # Convert BigQuery results to a list of dictionaries
    results_list = []
    for row in itertools.islice(bigquery_results, 5):
        results_list.append(dict(row))

    # Prepare the response data
    response_data = {
        'air_quality': {
            'grid_id': grid_id,
            'period': {
                'startTime': start_time.isoformat(),
                'endTime': end_time.isoformat(),
            },
            'air_quality_data': results_list,  # Adjust this based on your specific data structure
            # Add other data as needed based on your provided knowledge
        }
    }

    # Return the response data as JSON
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
