from PIL import Image, ImageDraw
import io
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pm25_database"]
collection = db["pm25_collection"]

# Example PM2.5 data (replace with your data)
pm25_data = [
    {"latitude": 40.7128, "longitude": -74.006, "pm25": 35},
    {"latitude": 34.0522, "longitude": -118.2437, "pm25": 65},
    # Add more data...
]

# Define image size
image_width = 1000
image_height = 500

# Create a blank image
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Define a function to map latitude and longitude to x and y coordinates
def map_to_pixel(latitude, longitude):
    x = int((longitude + 180) * (image_width / 360))
    y = int((90 - latitude) * (image_height / 180))
    return x, y

# Define a function to map PM2.5 values to AQI colors
def get_aqi_color(pm25):
    # Define your AQI scale and corresponding colors here
    AQI_scale = [(0, (0, 255, 0)), (50, (255, 255, 0))]
    for threshold, color in AQI_scale:
        if pm25 <= threshold:
            return color
    return (255, 0, 0)  # Default color for values exceeding AQI scale

# Plot PM2.5 data on the image
for data in pm25_data:
    x, y = map_to_pixel(data["latitude"], data["longitude"])
    # Get AQI color for PM2.5 value
    aqi_color = get_aqi_color(data["pm25"])
    # Plot pixel with AQI color
    draw.point((x, y), fill=aqi_color)

# Save the image to a temporary file
image_bytes = io.BytesIO()
image.save(image_bytes, format='PNG')
image_bytes.seek(0)

# Insert the image binary data and PM2.5 data into MongoDB
collection.insert_one({
    "image": image_bytes.read(),
    "pm25_data": pm25_data
})

# Close MongoDB connection
client.close()
