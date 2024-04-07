from flask import Flask, send_file
from PIL import Image, ImageDraw
import psycopg2
from configure import Config
from io import BytesIO

app = Flask(__name__)

# Function to calculate AQI
def calculate_aqi(pm25):
    # Placeholder AQI calculation logic
    if pm25 <= 12:
        aqi = (pm25 / 12) * 50
    elif pm25 <= 35.4:
        aqi = ((pm25 - 12) / (35.4 - 12)) * (100 - 51) + 51
    elif pm25 <= 55.4:
        aqi = ((pm25 - 35.4) / (55.4 - 35.4)) * (150 - 101) + 101
    elif pm25 <= 150.4:
        aqi = ((pm25 - 55.4) / (150.4 - 55.4)) * (200 - 151) + 151
    elif pm25 <= 250.4:
        aqi = ((pm25 - 150.4) / (250.4 - 150.4)) * (300 - 201) + 201
    elif pm25 <= 350.4:
        aqi = ((pm25 - 250.4) / (350.4 - 250.4)) * (400 - 301) + 301
    elif pm25 <= 500.4:
        aqi = ((pm25 - 350.4) / (500.4 - 350.4)) * (500 - 401) + 401
    else:
        aqi = 500
    return aqi

# Function to map AQI to RGB colors
def map_aqi_to_color(aqi):
    if aqi <= 50:
        return (0, 255, 0)  # Green
    elif aqi <= 100:
        return (255, 255, 0)  # Yellow
    elif aqi <= 150:
        return (255, 165, 0)  # Orange
    elif aqi <= 200:
        return (255, 0, 0)  # Red
    elif aqi <= 300:
        return (128, 0, 128)  # Purple
    else:
        return (128, 0, 0)  # Maroon

# Function to generate heatmap tile
def generate_heatmap_tile(pm25_data):
    # Image size for the tile
    tile_size = 256
    # Create a new blank image
    img = Image.new('RGB', (tile_size, tile_size), color='white')
    draw = ImageDraw.Draw(img)

    # Loop through PM2.5 data and draw points
    for pm25, centroid in pm25_data:
        aqi = calculate_aqi(pm25)
        color = map_aqi_to_color(aqi)
        lon, lat = centroid[0], centroid[1]
        x = int((lon + 180) * tile_size / 360)
        y = int((90 - lat) * tile_size / 180)
        draw.point((x, y), fill=color)

    return img

# Function to retrieve PM2.5 data from PostgreSQL
def retrieve_pm25_data(zoom, x, y):
    connection = psycopg2.connect(Config.POSTGRES_CONNECTION_URL)
    cursor = connection.cursor()

    # Example query to retrieve PM2.5 data based on zoom, x, and y
    cursor.execute("SELECT pm2_5, ST_X(centroid), ST_Y(centroid) FROM {} WHERE zoom = %s AND x = %s AND y = %s".format(Config.POSTGRES_TABLE),
                   (zoom, x, y))
    pm25_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return pm25_data

# API endpoint to serve heatmap tile
@app.route('/heatmap_tile/<int:zoom>/<int:x>/<int:y>.png')
def heatmap_tile(zoom, x, y):
    # Retrieve PM2.5 data from database based on zoom, x, and y
    pm25_data = retrieve_pm25_data(zoom, x, y)

    # Generate heatmap tile
    heatmap_img = generate_heatmap_tile(pm25_data)

    # Return the image file
    img_io = BytesIO()
    heatmap_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
