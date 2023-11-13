from flask import Flask, render_template, request
from configure import Config
from utils import fetch_air_quality_data, generate_report

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grid_id = request.form['grid_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time'] 
        page = 1

        air_quality_data = fetch_air_quality_data(grid_id, start_time, end_time,page)
        report_data = generate_report(air_quality_data)

        return render_template('report.html', report_data=report_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
