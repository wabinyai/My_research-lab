from flask import Flask, jsonify, request
from utils import fetch_air_quality_data, calculate_date_average_pm2_5, read_air_quality_data, calculate_diurnal_average_pm2_5, calculate_average_pm2_5_by_site, calculate_monthly_average_pm2_5, calculate_yearly_average_pm2_5,calculate_average_pm2_5_by_site
from datetime import datetime

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def get_air_quality_data():
    try:
        data = request.json  # Get JSON data from the request
        grid_id = data['grid_id']
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M')
        page = 1
        air_quality_data = fetch_air_quality_data(grid_id, start_time, end_time, page)
        # If data is available, process and return the results
        if air_quality_data:
            air_quality_data = read_air_quality_data(air_quality_data)
            avg_pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)
            top_PM_sites = avg_pm2_5_by_site.nlargest(5, "pm2_5_value")
            least_PM_sites = avg_pm2_5_by_site.nsmallest(5, "pm2_5_value")
            monthly_average_pm2_5 = calculate_monthly_average_pm2_5(air_quality_data)
            yearly_average_pm2_5 = calculate_yearly_average_pm2_5(air_quality_data)
            diurnal_average_pm2_5 = calculate_diurnal_average_pm2_5(air_quality_data)
            date_average_pm2_5 = calculate_date_average_pm2_5(air_quality_data)
            pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)
            # Prepare the response data in a structured format
            response_data = {
                'status': 'success',
                'air_quality':{
                'grid_id': grid_id,
                'period': {
                    'startTime': start_time.isoformat(),
                    'endTime': end_time.isoformat(),
                            },                
                'air_quality_data':air_quality_data,
                'top_PM_sites': top_PM_sites.to_dict(orient='records'),
                'least_PM_sites': least_PM_sites.to_dict(orient='records'),
                'monthly_average_pm2_5': monthly_average_pm2_5.to_dict(orient='records'),
                'yearly_average_pm2_5': yearly_average_pm2_5.to_dict(orient='records'),
                'diurnal_average_pm2_5': diurnal_average_pm2_5.to_dict(orient='records'),                
                'date_average_pm2_5':date_average_pm2_5.to_dict(orient='records'),
                'pm2_5_by_site':pm2_5_by_site.to_dict(orient='records')
            }
            }
             # Return the response data as JSON
            return jsonify(response_data)
        else:
            return jsonify({'message': 'No data available for the specified time range.'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
