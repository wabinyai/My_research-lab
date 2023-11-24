import requests

def get_pm25_data(latitude, longitude):
    api_url = f'https://platform.airqo.net/api/v2/predict/search?latitude={latitude}&longitude={longitude}&token=your_api_token'
    response = requests.get(api_url)
    data = response.json()
    return data
