from flask import Flask, jsonify, request
from utils import fetch_air_quality_data, query_bigquery, results_to_dataframe, get_data_for_moran
from datetime import datetime

app = Flask(__name__)

@app.route('/get_air_quality_data', methods=['POST'])
def get_air_quality_data():
    try:
        # Parse input data from Postman
        postman_data = request.get_json()
        grid_id = postman_data.get('grid_id')
        start_time_str = postman_data.get('start_time')
        end_time_str = postman_data.get('end_time')

        # Convert start_time and end_time to datetime objects
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)

        # Fetch site_ids using the provided grid_id and time range
        site_ids = fetch_air_quality_data(grid_id, start_time, end_time)

        if not site_ids:
            response_data = {
                'airquality': {
                    'status': 'error',
                    'message': 'No air quality data available for the specified parameters.'
                }
            }
            return jsonify(response_data)

        # Query BigQuery for air quality data based on site_ids and time range
        results = query_bigquery(site_ids, start_time, end_time)

        if results is None:
            response_data = {
                'airquality': {
                    'status': 'error',
                    'message': 'Error querying BigQuery for air quality data.'
                }
            }
            return jsonify(response_data)

        # Convert results to DataFrame and perform necessary data manipulations
        df = results_to_dataframe(results)

        # Get GeoDataFrame for Local Moran's I analysis
        gdf = get_data_for_moran(df)

        # Construct the final response data
        response_data = {
            'airquality': {
                'status': 'success',
                'grid_id': grid_id,
                'site_ids': site_ids,
                'period': {
                    'startTime': start_time.isoformat(),
                    'endTime': end_time.isoformat(),
                },
                'gdf': gdf.to_json()  # Convert GeoDataFrame to JSON
            }
        }

        return jsonify(response_data)

    except Exception as e:
        response_data = {
            'airquality': {
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }
        }
        return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
