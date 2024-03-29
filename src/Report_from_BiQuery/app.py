from flask import Flask, request, jsonify
from datetime import datetime
import logging
from utils import (fetch_air_quality_data, 
                                         pm_by_city,pm_by_country,
                                         pm_by_region, monthly_mean_pm_site_name,
                                         datetime_pm2_5, mean_pm2_5_by_month_year, 
                                         mean_pm2_5_by_month_name, query_bigquery, 
                                         mean_pm2_5_by_month, results_to_dataframe,
                                           mean_pm2_5_by_year, mean_daily_pm2_5, 
                                           mean_pm2_5_by_site_name, mean_pm2_5_by_hour)
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

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
        logging.error('Invalid date format: %s', e)
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
            monthly_mean_pm_by_site_name =  monthly_mean_pm_site_name(processed_data)
            mean_pm_by_city=pm_by_city(processed_data)
            mean_pm_by_country =pm_by_country(processed_data)
            mean_pm_by_region=pm_by_region(processed_data)

            # Log some information for debugging or monitoring
            logging.info('Successfully processed air quality data for grid_id %s', grid_id)

            # Prepare the response data in a structured format
            response_data = {
                'airquality': {
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
                'diurnal': hour_mean_pm2_5.to_dict(orient='records'),
                'annual_pm': mean_pm2_5_year.to_dict(orient='records'),
                'monthly_pm': pm2_5_by_month.to_dict(orient='records'),
                'pm_by_month_year': pm2_5_by_month_year.to_dict(orient='records'),
                'pm_by_month_name': pm2_5_by_month_name.to_dict(orient='records'),
                'monthly_mean_pm_site_name': monthly_mean_pm_by_site_name.to_dict(orient='records'),
                'mean_pm_by_city': mean_pm_by_city.to_dict(orient='records'),   
                'mean_pm_by_country': mean_pm_by_country.to_dict(orient='records'),
                'mean_pm_by_region': mean_pm_by_region.to_dict(orient='records'),
                }

            }

            return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
