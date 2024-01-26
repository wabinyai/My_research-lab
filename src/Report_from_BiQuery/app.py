from flask import Flask, request, jsonify
from datetime import datetime
from utils import fetch_air_quality_data,datetime_pm2_5, mean_pm2_5_by_month_year, mean_pm2_5_by_month_name, query_bigquery, mean_pm2_5_by_month, results_to_dataframe, mean_pm2_5_by_year, mean_daily_pm2_5, mean_pm2_5_by_site_name, mean_pm2_5_by_hour

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def air_quality_data():
    data = request.get_json()

    grid_id = data.get("grid_id", "")
    start_time_str = data.get("start_time", "")
    end_time_str = data.get("end_time", "")

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError as e:
        return jsonify({'error': 'Invalid date format'}), 400

    site_ids = fetch_air_quality_data(grid_id, start_time, end_time)

    if site_ids:
        results = query_bigquery(site_ids, start_time, end_time)
        if results is not None:
            processed_data = results_to_dataframe(results)
            daily_mean_pm2_5 = mean_daily_pm2_5(processed_data)
            datetime_mean_pm2_5 = datetime_pm2_5(processed_data)
            site_mean_pm2_5 = mean_pm2_5_by_site_name(processed_data)
            hour_mean_pm2_5 = mean_pm2_5_by_hour(processed_data)
            mean_pm2_5_year = mean_pm2_5_by_year(processed_data)
            pm2_5_by_month = mean_pm2_5_by_month(processed_data)
            pm2_5_by_month_name = mean_pm2_5_by_month_name(processed_data)
            pm2_5_by_month_year = mean_pm2_5_by_month_year(processed_data)
             

            # Prepare the response data in a structured format
            response_data = {
                    'airquality':'air_quality',
                    'status': 'success',
                    'grid_id': grid_id,
                    'site_ids': site_ids,
                    'period': {
                        'startTime': start_time.isoformat(),
                        'endTime': end_time.isoformat(),
                    },
                    'daily_mean_pm': daily_mean_pm2_5.to_dict(orient='records'),
                    'datetime_mean_pm': datetime_mean_pm2_5.to_dict(orient='records'),
                    'site_mean_pm': site_mean_pm2_5.to_dict(orient='records'),
                    'hour_mean_pm': hour_mean_pm2_5.to_dict(orient='records'),
                    'mean_pm_year': mean_pm2_5_year.to_dict(orient='records'),
                    'pm_by_month': pm2_5_by_month.to_dict(orient='records'),
                    'pm_by_month_year': pm2_5_by_month_year.to_dict(orient='records'),
                    'pm_by_month_name': pm2_5_by_month_name.to_dict(orient='records'),
               
            }

            return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
