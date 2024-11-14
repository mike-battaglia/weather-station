import os
import smbus2
import bme280
from datetime import datetime
import pytz
from math import log, exp
import pandas as pd
import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Get the WP API key from environment variables
wp_domain = os.getenv('WEATHER_DOMAIN')
wp_api_key = os.getenv('WEATHER_API_KEY')
if not wp_api_key:
    raise EnvironmentError("Please set the WEATHER_API_KEY environment variable")

# Sensor settings
port = 1
address = 0x77  # Change to 0x77 if your sensor uses that address
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# Timezone settings
timezone = pytz.timezone('America/Chicago')

def get_sensor_data():
    try:
        print("Getting sensor data...")
        sensor_data = bme280.sample(bus, address, calibration_params)
        sensor_temp_c = sensor_data.temperature
        sensor_humidity = sensor_data.humidity
        sensor_pressure = sensor_data.pressure
        timestamp = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Sensor Data - Temperature: {sensor_temp_c}°C, Humidity: {sensor_humidity}%, Pressure: {sensor_pressure} hPa")
        return sensor_temp_c, sensor_humidity, sensor_pressure, timestamp
    except Exception as e:
        print(f"Error getting sensor data: {e}")
        return None, None, None, None
