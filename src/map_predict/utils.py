import requests
from configure import Config

def get_pm25_data(latitude, longitude) -> list:
    # Convert start_time and end_time to ISO format
#    start_time_iso = start_time.isoformat() + 'Z'
#    end_time_iso = end_time.isoformat() + 'Z'
    
    grid_params = {
        "token": Config.AIRQO_API_TOKEN,
        "latitude": latitude,
        "longitude": longitude,

    }
    
    url = f"https://platform.airqo.net/api/v2/predict/search?"
     
    grid_response = requests.get(url, params=grid_params)
    if grid_response.status_code == 200:
        data = grid_response.json()
        return data["data"]
    else:
        # Handle the response error, e.g., raise an exception or return an empty list
        return []
