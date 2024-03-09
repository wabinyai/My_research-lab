from flask import Flask, render_template, request
from utils import fetch_data_from_api, get_data_for_getis, Getis_Ord_Local_regression, plot_Getis_Ord_local
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grid_id = request.form['grid_id']
        start_time = datetime.fromisoformat(request.form['start_time'])
        end_time = datetime.fromisoformat(request.form['end_time'])

        data = fetch_data_from_api(grid_id, start_time, end_time)

        if data:
            gdf = get_data_for_getis(data)
            
            if 'calibratedValue' in gdf.columns:
                gdf = gdf.dropna(subset=['calibratedValue'])

                g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90 = Getis_Ord_Local_regression(gdf)

                #plot_Getis_Ord_local(g_local, significant_hot_spots_99, significant_hot_spots_95, significant_hot_spots_90, significant_cold_spots_99, significant_cold_spots_95, significant_cold_spots_90, gdf)

                return render_template('index.html', gdf=gdf.to_html())
            else:
                return render_template('index.html', message="No measurements for this search.")
        else:
            return render_template('index.html', message="Failed to fetch data from the API.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
