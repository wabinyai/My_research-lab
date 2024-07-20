from flask import Flask, request, jsonify, render_template
import pandas as pd
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Function to load data
def load_data():
    df = pd.read_json('aqi_data.json')
    return df

# Function to map pm2.5 levels to AQI colors
def pm25_to_aqi_color(pm25_level):
    if pm25_level <= 1:
        return 'green'
    elif pm25_level <= 2:
        return 'yellow'
    elif pm25_level <= 3:
        return 'orange'
    elif pm25_level <= 4:
        return 'red'
    elif pm25_level <= 5:
        return 'purple'
    else:
        return 'maroon'

@app.route('/heatmap-data', methods=['GET'])
def heatmap_data():
    try:
        lat_north = float(request.args.get('lat_north'))
        lat_south = float(request.args.get('lat_south'))
        lon_east = float(request.args.get('lon_east'))
        lon_west = float(request.args.get('lon_west'))

        df = load_data()

        df_filtered = df[(df['latitude'] >= lat_south) & (df['latitude'] <= lat_north) &
                         (df['longitude'] >= lon_west) & (df['longitude'] <= lon_east)]

        features = [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['longitude'], row['latitude']]
            },
            'properties': {
                'pm25_level': row['pm25_level'],
                'color': pm25_to_aqi_color(row['pm25_level'])
            }
        } for index, row in df_filtered.iterrows()]

        geojson_data = {
            'type': 'FeatureCollection',
            'features': features
        }

        return jsonify(geojson_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    mapbox_access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
    return render_template('index.html', mapbox_access_token=mapbox_access_token)

if __name__ == '__main__':
    app.run(debug=True)