from flask import Flask
from controller import heatmap_tile_and_save

app = Flask(__name__)

# API endpoint to serve heatmap tile and save it to a new PostgreSQL table
app.add_url_rule('/heatmap_tile_and_save/<int:zoom>/<int:x>/<int:y>', 'heatmap_tile_and_save', heatmap_tile_and_save)

if __name__ == '__main__':
    app.run(debug=True)
