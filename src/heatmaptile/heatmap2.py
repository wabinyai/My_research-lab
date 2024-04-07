from flask import Flask, send_file
from io import BytesIO
import pymongo
import folium
from PIL import Image

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pm25_database"]
collection = db["pm25_collection"]

app = Flask(__name__)

@app.route('/map')
def display_image_on_map(image_id):
    # Retrieve image and PM2.5 data from MongoDB
    image_data = collection.find_one({"_id": image_id})
    pm25_data = image_data["pm25_data"]
    image_binary = image_data["image"]
    
    # Convert image binary data to PIL Image
    image = Image.open(BytesIO(image_binary))
    
    # Create a map using Folium
    map_center = [sum([data["latitude"] for data in pm25_data]) / len(pm25_data),
                  sum([data["longitude"] for data in pm25_data]) / len(pm25_data)]
    my_map = folium.Map(location=map_center, zoom_start=5)
    
    # Add markers for PM2.5 data
    for data in pm25_data:
        folium.Marker(location=[data["latitude"], data["longitude"]],
                      popup=f"PM2.5: {data['pm25']}").add_to(my_map)
    
    # Convert PIL Image to bytes
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    # Add the image as an overlay on the map
    folium.raster_layers.ImageOverlay(image_bytes, bounds=[[min([data["latitude"] for data in pm25_data]),
                                                            min([data["longitude"] for data in pm25_data])],
                                                           [max([data["latitude"] for data in pm25_data]),
                                                            max([data["longitude"] for data in pm25_data])]],
                                      opacity=0.7).add_to(my_map)
    
    # Save the map as an HTML file
    html_file_path = f"map_{image_id}.html"
    my_map.save(html_file_path)
    
    # Serve the HTML file
    return send_file(html_file_path, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)
