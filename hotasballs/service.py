# -*- coding: utf-8 -*-
import os
import requests

DARKSKY_SECRET_KEY = os.environ.get('DARKSKY_SECRET_KEY')

def handler(event, context):
    lon = event.get('lon')
    lat = event.get('lat')
    city = event.get('city')

    DARKSKY_URL = f'https://api.darksky.net/forecast/{DARKSKY_SECRET_KEY}/{lon},{lat}'
    payload = {
        'units': 'si',
        'exclude': 'hourly',
    }
    weather = requests.get(DARKSKY_URL, params=payload).json()

    today = weather['daily']['data'][0]

    temperatureHigh = round(today['temperatureHigh'], 1)
    apparentTemperatureHigh = round(today['apparentTemperatureHigh'], 1)
    humidity = round(today['humidity'] * 100)

    if apparentTemperatureHigh < 30:
        message = f"It's not that hot in {city} today, chill out."
    else:
        message = f"Man, it's hot as balls in {city} today! 🔥🎱"
        if apparentTemperatureHigh - temperatureHigh > 1:
            message += f"\n{temperatureHigh}°C (feels like {apparentTemperatureHigh}°C🔥) with {humidity}% humidity💦"
        else:
            message += f"\n{temperatureHigh}°C🔥 with {humidity}% humidity💦"

    return message
