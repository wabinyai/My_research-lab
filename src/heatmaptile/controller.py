from flask import send_file
from database import retrieve_pm25_data, generate_and_save_heatmap_tile

def heatmap_tile_and_save(zoom, x, y):
    # Retrieve PM2.5 data from database based on zoom, x, and y
    pm25_data = retrieve_pm25_data(zoom, x, y)

    # Generate and save heatmap tile to new PostgreSQL table
    generate_and_save_heatmap_tile(pm25_data)

    # Return success message
    return "Heatmap tile saved to new PostgreSQL table."
