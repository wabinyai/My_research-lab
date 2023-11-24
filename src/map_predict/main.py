
import requests
import json
from utils import get_pm25_data


def get_pm25_data_route():
    latitude = 0.912314
    longitude = 32.599872
    pm25_data = get_pm25_data(latitude, longitude)
    return json(pm25_data)

 