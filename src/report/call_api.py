import requests

url = "http://127.0.0.1:5000/report"
data = {
    'grid_id': '659d036497e611001236cd1b',
    'start_time': '2023-09-01T00:00',
    'end_time': '2024-01-22T00:00',
#    'top_location': 5,
 #   'least_location': 5
}

response = requests.post(url, data=data)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}, {response.text}")
