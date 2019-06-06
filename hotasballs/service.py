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

    temperatureHigh = today['temperatureHigh']
    apparentTemperatureHigh = today['apparentTemperatureHigh']
    humidity = today['humidity']

    if apparentTemperatureHigh < 35:
        message = "It's not that hot in Tokyo today, chill out."
    else:
        message = "Man, it's hot as balls in Tokyo today!"
        if apparentTemperatureHigh - temperatureHigh > 1:
            message += f"\n{temperatureHigh:.1f}°C ({apparentTemperatureHigh:.1f}°C felt) with {humidity * 100:.0f}% humidity"
        else:
            message += f"\n{temperatureHigh:.1f}°C with {humidity * 100:.0f}% humidity"

    return message