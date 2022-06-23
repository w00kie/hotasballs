# -*- coding: utf-8 -*-
import os
from typing import Optional
import random
import requests
import tweepy

WEATHER_SECRET_KEY: str = os.environ.get('WEATHER_SECRET_KEY')
HOT_THRESHOLD: int = int(os.environ.get('HOT_THRESHOLD', 35))
COLD_THRESHOLD: int = int(os.environ.get('COLD_THRESHOLD', 28))
TWITTER_CONSUMER_KEY: str = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET: str = os.environ.get('TWITTER_CONSUMER_SECRET')


class Weather:
    '''Get data we're interested in from weather forecast json and format it.'''
    temperatureHigh: float
    apparentTemperatureHigh: float
    humidity: int

    def __init__(self, data: dict) -> None:
        self.temperatureHigh = round(data['tempmax'], 1)
        self.apparentTemperatureHigh = round(data['feelslikemax'], 1)
        self.humidity = round(data['humidity'])


def get_weather(lat: float, lon: float, city: str) -> object:
    '''Call Weather API and return the weather data we need.'''
    WEATHER_URL = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}'
    payload = {
        'unitGroup': 'metric',
        'key': WEATHER_SECRET_KEY,
        'contentType': 'json',
    }
    forecast = requests.get(WEATHER_URL, params=payload).json()

    # Only interested in today's forecast
    today = forecast['days'][0]
    
    return Weather(today)


def generate_message(weather: Weather, city: str) -> Optional[str]:
    '''Generate a cool message from local weather data.'''
    if weather.apparentTemperatureHigh < COLD_THRESHOLD:
        # If too cold, nothing to say
        message = None
    elif weather.apparentTemperatureHigh < HOT_THRESHOLD:
        # If hot but not hot as balls
        qualifier = random.choice([
            'not that hot',
            'not that sweaty',
            'almost livable',
            'not yet scorching',
            'barely sweltering',
            'fairly bearable',
        ])
        ending = random.choice([
            'chill out',
            'stop whining',
            'yolo',
        ])
        message = f"It's {qualifier} in {city} today, {ending}..."
    else:
        # If it's hot as balls
        message = f"Man, it's hot as balls in {city} today! 🔥🎱\n"
        if weather.apparentTemperatureHigh - weather.temperatureHigh > 1:
            message += f"{weather.temperatureHigh}°C (feels like {weather.apparentTemperatureHigh}°C🔥) with {weather.humidity}% humidity💦"
        else:
            message += f"{weather.temperatureHigh}°C🔥 with {weather.humidity}% humidity💦"
    
    return message


def handler(event, context):
    '''The lambda handler that posts to twitter.'''
    # Parse event data
    lon: float = event.get('lon')
    lat: float = event.get('lat')
    city: str = event.get('city')
    access_token: str = event.get('access_token')
    access_token_secret: str = event.get('access_token_secret')

    weather = get_weather(lat, lon, city)

    message = generate_message(weather, city)

    # Post to twitter only if we have a message
    if message:
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(message)

    return message
