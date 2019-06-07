# -*- coding: utf-8 -*-
import os
import requests
import tweepy

DARKSKY_SECRET_KEY = os.environ.get('DARKSKY_SECRET_KEY')
HOT_THRESHOLD = int(os.environ.get('HOT_THRESHOLD', 35))
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

def handler(event, context):
    lon = event.get('lon')
    lat = event.get('lat')
    city = event.get('city')
    access_token = event.get('access_token')
    access_token_secret = event.get('access_token_secret')

    DARKSKY_URL = f'https://api.darksky.net/forecast/{DARKSKY_SECRET_KEY}/{lat},{lon}'
    payload = {
        'units': 'si',
        'exclude': 'hourly',
    }
    weather = requests.get(DARKSKY_URL, params=payload).json()

    today = weather['daily']['data'][0]

    temperatureHigh = round(today['temperatureHigh'], 1)
    apparentTemperatureHigh = round(today['apparentTemperatureHigh'], 1)
    humidity = round(today['humidity'] * 100)

    if apparentTemperatureHigh < HOT_THRESHOLD:
        message = f"It's not that hot in {city} today, chill out."
    else:
        message = f"Man, it's hot as balls in {city} today! 🔥🎱"
        if apparentTemperatureHigh - temperatureHigh > 1:
            message += f"\n{temperatureHigh}°C (feels like {apparentTemperatureHigh}°C🔥) with {humidity}% humidity💦"
        else:
            message += f"\n{temperatureHigh}°C🔥 with {humidity}% humidity💦"

    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)

    return message
