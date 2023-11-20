from flask import Flask, render_template, request
from utils import fetch_air_quality_data, read_air_quality_data, calculate_average_pm2_5_by_site, calculate_monthly_average_pm2_5
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grid_id = request.form['grid_id']
        start_time = datetime.strptime(request.form.get('start_time'), '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form.get('end_time'), '%Y-%m-%dT%H:%M')
        page = 1
        top_location = int(request.form['top_location'])  # Convert to integer
        least_location = int(request.form['least_location'])  # Convert to integer

        data = fetch_air_quality_data(grid_id, start_time, end_time, page)

        if data:
            air_quality_data = read_air_quality_data(data)
            avg_pm2_5_by_site = calculate_average_pm2_5_by_site(air_quality_data)

            top_PM_sites = avg_pm2_5_by_site.nlargest(top_location, "pm2_5_value")
            least_PM_sites = avg_pm2_5_by_site.nsmallest(least_location, "pm2_5_value")

            # Calculate monthly average PM2.5 data
            monthly_average_pm2_5 = calculate_monthly_average_pm2_5(air_quality_data)

            # Pass additional variables to the template
            return render_template('report.html', 
                                   grid_id=grid_id,
                                   month=start_time.month,
                                   startTime=start_time,
                                   endTime=end_time,
                                   top_PM_sites=top_PM_sites, 
                                   least_PM_sites=least_PM_sites,
                                   monthly_average_pm2_5=monthly_average_pm2_5)
        else:
            return render_template('index.html', message="No data available for the specified time range.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
