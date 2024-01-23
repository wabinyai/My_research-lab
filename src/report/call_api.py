import requests
import json

url = "http://127.0.0.1:5000/report"
data = {
    "grid_id": "659d036497e611001236cd1b",
    "start_time": "2024-01-12T00:00",
    "end_time": "2024-01-21T00:00",
}

headers = {'Content-Type': 'application/json'}  # Set the content type to JSON

# Convert the data to JSON format
json_data = json.dumps(data)

response = requests.post(url, data=json_data, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}, {response.text}")
