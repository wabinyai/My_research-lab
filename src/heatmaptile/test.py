from flask import Flask
import psycopg2
from PIL import Image, ImageDraw
from io import BytesIO
from controller import generate_and_save_heatmap_tile

app = Flask(__name__)

# Define your generate_and_save_heatmap_tile function here


@app.route('/generate_heatmap_and_save_to_postgres')
def generate_heatmap_and_save_to_postgres():
    # Mocking sample PM2.5 data
    pm25_data = [(10, (0.283761, 32.246138)), (10, (0.530947, 32.345015))]  # Example data

    generate_and_save_heatmap_tile(pm25_data)

    return "Heatmap generated and saved to PostgreSQL successfully!"


if __name__ == "__main__":
    app.run(debug=True)
