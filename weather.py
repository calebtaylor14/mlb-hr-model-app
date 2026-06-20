import requests

def get_weather_score():

    # Yadkinville, NC default (can change later)
    lat = 36.1348
    lon = -80.6598

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,wind_speed_10m"

    response = requests.get(url)
    data = response.json()

    temp = data["hourly"]["temperature_2m"][0]
    wind = data["hourly"]["wind_speed_10m"][0]

    # Convert to HR-friendly score
    score = 0

    # Temperature boost
    if temp >= 85:
        score += 3
    elif temp >= 75:
        score += 2
    else:
        score += 1

    # Wind boost
    if wind >= 15:
        score += 2
    elif wind >= 8:
        score += 1
    else:
        score += 0

    return min(score, 5)
