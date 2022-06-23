import os
import json
from pathlib import Path
from unittest import TestCase, mock
from dotenv import load_dotenv
import requests_mock
import tweepy

load_dotenv()

from hotasballs.hotasballs import service


class HotAsBallsTest(TestCase):
    def setUp(self):
        self.weather_data = json.load(
            open(Path(__file__).parent / 'weather_data.json', 'r'))
        self.lat = 35.640432
        self.lon = 139.728833
        self.city = 'Tokyo'
        event_input = {
            'lat': self.lat,
            'lon': self.lon,
            'city': self.city,
            'access_token': 'token',
            'access_token_secret': 'secret',
        }
        event_template = json.load(
            open(Path(__file__).parent / 'cloudwatch_event.json', 'r'))
        self.event = {**event_template, **event_input}
    
    def testTestEnv(self):
        '''Test that we have proper environment variables setup.'''
        self.assertEqual(service.HOT_THRESHOLD, 35)
        self.assertEqual(service.WEATHER_SECRET_KEY, 'secretkey')

    def testWeatherGet(self):
        '''Test that we can grab data from weather API and format it.'''
        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.city}?unitGroup=metric&key={os.getenv('WEATHER_SECRET_KEY')}&contentType=json",
                json=self.weather_data
            )
            weather = service.get_weather(self.lat, self.lon, self.city)
            self.assertEqual(weather.temperatureHigh, 28.1)
            self.assertEqual(weather.apparentTemperatureHigh, 29.0)
            self.assertEqual(weather.humidity, 78)
    
    def testColdMessage(self):
        '''Test message creation when too cold.'''
        w = service.Weather({
            'tempmax': 23.4,
            'feelslikemax': 24.0,
            'humidity': 85,
        })
        self.assertEqual(service.generate_message(w, 'Tokyo'), None)

    def testWarmMessage(self):
        '''Test message creation when just warm.'''
        w = service.Weather({
            'tempmax': 23.4,
            'feelslikemax': 29.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertNotIn('Hot as balls', message)

    def testHotMessage(self):
        '''Test message creation when it's hot as balls.'''
        w = service.Weather({
            'tempmax': 35.8,
            'feelslikemax': 36.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertIn('hot as balls', message)
        self.assertNotIn('feels like', message)

    def testHotFeltMessage(self):
        '''Test message creation when it's hot as balls and apparent temp gap.'''
        w = service.Weather({
            'tempmax': 29.4,
            'feelslikemax': 36.3,
            'humidity': 85,
        })
        message = service.generate_message(w, 'Tokyo')
        self.assertIn('Tokyo', message)
        self.assertIn('hot as balls', message)
        self.assertIn('feels like', message)

    @mock.patch.object(tweepy.API, 'update_status')
    def testFullHandler(self, mock_update_status):
        '''Test the full handler including twitter.'''
        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.city}?unitGroup=metric&key={os.getenv('WEATHER_SECRET_KEY')}&contentType=json",
                json=self.weather_data
            )
            output = service.handler(self.event, None)

            # Check message is as expected
            self.assertIn('Tokyo', output)
            # Check that Twitter was called
            mock_update_status.assert_called_with(output)
