from flask import Flask
from controller import heatmap_tile_and_save

app = Flask(__name__)

def generate_and_save_heatmap_tile():
    # Function to generate and save heatmap tile to PostgreSQL
    return  heatmap_tile_and_save

if __name__ == '__main__':
    generate_and_save_heatmap_tile()  # Call the function to generate and save heatmap tile
    app.run(debug=True)
