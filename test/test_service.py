import os
import json
from pathlib import Path
from unittest import TestCase, mock
from dotenv import load_dotenv
import requests_mock

load_dotenv()

from hotasballs.hotasballs import service


class HotAsBallsTest(TestCase):
    def setUp(self):
        self.weather_data = json.load(open(Path(__file__).parent / 'weather_data.json', 'r'))
        self.lat = 35.640432
        self.lon = 139.728833
    
    def testTestEnv(self):
        '''Test that we have proper environment variables setup.'''
        self.assertEqual(service.HOT_THRESHOLD, 35)
        self.assertEqual(service.DARKSKY_SECRET_KEY, 'darkskysecret')

    def testWeatherGet(self):
        '''Test that we can grab data from Darksky and format it.'''
        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://api.darksky.net/forecast/{os.getenv('DARKSKY_SECRET_KEY')}/{self.lat},{self.lon}?units=si&exclude=hourly",
                json=self.weather_data
            )
            weather = service.get_weather(self.lat, self.lon)
            self.assertEqual(weather.temperatureHigh, 23.4)
            self.assertEqual(weather.apparentTemperatureHigh, 24.0)
            self.assertEqual(weather.humidity, 85)
    
    def testColdMessage(self):
        '''Test message creation when too cold.'''
        w = service.Weather({
            'temperatureHigh': 23.4,
            'apparentTemperatureHigh': 24.0,
            'humidity': 85,
        })
        self.assertEqual(service.generate_message(w, 'Tokyo'), None)

    def testWarmMessage(self):
        '''Test message creation when just warm.'''
        w = service.Weather({
            'temperatureHigh': 23.4,
            'apparentTemperatureHigh': 29.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertNotIn('Hot as balls', message)

    def testHotMessage(self):
        '''Test message creation when it's hot as balls.'''
        w = service.Weather({
            'temperatureHigh': 35.8,
            'apparentTemperatureHigh': 36.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertIn('hot as balls', message)
        self.assertNotIn('feels like', message)

    def testHotFeltMessage(self):
        '''Test message creation when it's hot as balls and apparent temp gap.'''
        w = service.Weather({
            'temperatureHigh': 29.4,
            'apparentTemperatureHigh': 36.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertIn('hot as balls', message)
        self.assertIn('feels like', message)
