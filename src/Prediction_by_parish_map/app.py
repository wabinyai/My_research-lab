from flask import Flask, render_template, request
from configure import Config
import branca.colormap as cm
import folium
import geopandas as gpd
from utils import fetch_data_from_api, get_grouped_data_for_pm
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def render_map():
    if request.method == 'POST':
        # Get form data
        grid_id = request.form['grid_id']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        # Fetch data from the AirQo API
        df_u22 = fetch_data_from_api(grid_id, start_time, end_time, page=1)

        # Your existing map creation logic
        df_u2 = get_grouped_data_for_pm(df_u22)
        print(df_u2)

        # Create a folium map centered around the first data point
        map = folium.Map(location=[df_u2['latitude'].iloc[0], df_u2['longitude'].iloc[0]], zoom_start=12)

        # Add air quality data markers to the map
        for _, row in df_u2.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']],
                                popup=f"Calibrated Value: {row['calibratedValue']}",
                                radius=10,
                                color='blue',  # Change this to your color logic
                                fill=True,
                                fill_color='blue',  # Change this to your color logic
                                opacity=0.7,
                                fill_opacity=0.8
                                ).add_to(map)

        # Render the HTML template with the Folium map
        return render_template('index.html', map=map._repr_html_())

    # Render the default form
    return render_template('index.html', map=None)

if __name__ == '__main__':
    app.run(debug=True)
