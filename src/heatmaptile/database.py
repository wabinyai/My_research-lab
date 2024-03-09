import psycopg2
from configure import Config
from utils import calculate_aqi, map_aqi_to_color
from PIL import Image, ImageDraw
from io import BytesIO

def retrieve_pm25_data(zoom, x, y):
    connection = psycopg2.connect(Config.POSTGRES_CONNECTION_URL)
    cursor = connection.cursor()

    cursor.execute("SELECT pm2_5, centroid FROM {} WHERE zoom = %s AND x = %s AND y = %s".format(Config.POSTGRES_TABLE),
                   (zoom, x, y))
    pm25_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return pm25_data

def generate_and_save_heatmap_tile(pm25_data):
    tile_size = 256
    img = Image.new('RGB', (tile_size, tile_size), color='white')
    draw = ImageDraw.Draw(img)

    for pm25, centroid in pm25_data:
        aqi = calculate_aqi(pm25)
        color = map_aqi_to_color(aqi)
        lon, lat = centroid[0], centroid[1]
        x = int((lon + 180) * tile_size / 360)
        y = int((90 - lat) * tile_size / 180)
        draw.point((x, y), fill=color)

    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    image_data = img_io.read()

    connection = psycopg2.connect(Config.POSTGRES_CONNECTION_URL)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO {} (image_data) VALUES (%s)".format(Config.POSTGRES_TABLE), (image_data,))
    connection.commit()
    cursor.close()
    connection.close()
