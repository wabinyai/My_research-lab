def calculate_aqi(pm25):
    # Placeholder AQI calculation logic
    if pm25 <= 12:
        aqi = (pm25 / 12) * 50
    elif pm25 <= 35.4:
        aqi = ((pm25 - 12) / (35.4 - 12)) * (100 - 51) + 51
    elif pm25 <= 55.4:
        aqi = ((pm25 - 35.4) / (55.4 - 35.4)) * (150 - 101) + 101
    elif pm25 <= 150.4:
        aqi = ((pm25 - 55.4) / (150.4 - 55.4)) * (200 - 151) + 151
    elif pm25 <= 250.4:
        aqi = ((pm25 - 150.4) / (250.4 - 150.4)) * (300 - 201) + 201
    elif pm25 <= 350.4:
        aqi = ((pm25 - 250.4) / (350.4 - 250.4)) * (400 - 301) + 301
    elif pm25 <= 500.4:
        aqi = ((pm25 - 350.4) / (500.4 - 350.4)) * (500 - 401) + 401
    else:
        aqi = 500
    return aqi


def map_aqi_to_color(aqi):
    if aqi <= 50:
        return (0, 255, 0)  # Green
    elif aqi <= 100:
        return (255, 255, 0)  # Yellow
    elif aqi <= 150:
        return (255, 165, 0)  # Orange
    elif aqi <= 200:
        return (255, 0, 0)  # Red
    elif aqi <= 300:
        return (128, 0, 128)  # Purple
    else:
        return (128, 0, 0)  # Maroon