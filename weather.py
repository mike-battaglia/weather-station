import smbus2
import bme280
import requests
from datetime import datetime
import pytz
from math import log, exp
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the API key from environment variables
api_key = os.getenv('WEATHER_API_KEY')
if not api_key:
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
        data = bme280.sample(bus, address, calibration_params)
        temp_c = data.temperature
        humidity = data.humidity
        pressure = data.pressure
        timestamp = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        return temp_c, humidity, pressure, timestamp
    except Exception as e:
        logger.error(f"Error reading sensor data: {e}")
        return None, None, None, None

def calculate_dew_point(temp_c, humidity):
    # Dew Point calculation using Magnus formula
    b = 17.62
    c = 243.12
    gamma = (b * temp_c / (c + temp_c)) + log(humidity / 100.0)
    dew_point = (c * gamma) / (b - gamma)
    return dew_point

def calculate_feels_like(temp_c, humidity, wind_speed_mps):
    # Determine which formula to use
    if temp_c >= 26.7 and humidity >= 40:
        # Heat Index calculation (using Celsius)
        hi_c = -8.78469475556 + 1.61139411 * temp_c + 2.33854883889 * humidity
        hi_c += -0.14611605 * temp_c * humidity - 0.012308094 * temp_c**2
        hi_c += -0.0164248277778 * humidity**2 + 0.002211732 * temp_c**2 * humidity
        hi_c += 0.00072546 * temp_c * humidity**2 - 0.000003582 * temp_c**2 * humidity**2
        feels_like_c = hi_c
    elif temp_c <= 10 and wind_speed_mps > 1.3:
        # Wind Chill calculation (using Celsius)
        feels_like_c = 13.12 + 0.6215 * temp_c - 11.37 * wind_speed_mps**0.16 + 0.3965 * temp_c * wind_speed_mps**0.16
    else:
        # Apparent Temperature calculation
        e = humidity / 100 * 6.105 * exp(17.27 * temp_c / (237.7 + temp_c))
        feels_like_c = temp_c + 0.33 * e - 0.70 * wind_speed_mps - 4.00

    return feels_like_c

def get_additional_data():
    # Free API: Open-Meteo
    api_url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=31.3256&longitude=-95.3677&current_weather=true&"
        "hourly=cloudcover,visibility"
    )
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            current_weather = data.get('current_weather', {})
            wind_speed = current_weather.get('windspeed', 0)
            wind_direction = current_weather.get('winddirection')
            cloud_cover = data.get('hourly', {}).get('cloudcover', [None])[0]
            visibility = data.get('hourly', {}).get('visibility', [None])[0]
            uv_index = data.get('hourly', {}).get('uv_index', [None])[0]
            return wind_speed, wind_direction, uv_index, cloud_cover, visibility
        else:
            logger.error(f"Failed to get additional weather data: {response.status_code}")
            return None, None, None, None, None
    except Exception as e:
        logger.error(f"Error fetching additional data: {e}")
        return None, None, None, None, None

def convert_to_imperial(temp_c, pressure, wind_speed_mps, visibility_m):
    temp_f = temp_c * 9/5 + 32
    pressure_inhg = pressure * 0.02953
    wind_speed_mph = wind_speed_mps * 2.23694 if wind_speed_mps and wind_speed_mps > 0 else 0
    visibility_miles = visibility_m * 0.000621371 if visibility_m is not None else None
    return temp_f, pressure_inhg, wind_speed_mph, visibility_miles

def send_data(data):
    url = 'https://garyweather.com/wp-json/custom/v1/weather'
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key  # Use the API key defined above
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        logger.info(f"Data sent. Server responded with: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send data: {e}")

def main():
    temp_c, humidity, pressure, timestamp = get_sensor_data()
    if temp_c is None or humidity is None or pressure is None:
        logger.error("Sensor data is unavailable. Exiting.")
        return

    dew_point_c = calculate_dew_point(temp_c, humidity)
    wind_speed, wind_direction, uv_index, cloud_cover, visibility = get_additional_data()

    feels_like_c = calculate_feels_like(temp_c, humidity, wind_speed)

    # Convert units to imperial
    temp_f, pressure_inhg, wind_speed_mph, visibility_miles = convert_to_imperial(temp_c, pressure, wind_speed, visibility)
    dew_point_f = dew_point_c * 9/5 + 32
    feels_like_f = feels_like_c * 9/5 + 32

    data = {
        'timestamp': timestamp,
        'temperature_f': round(temp_f, 2),
        'humidity_percent': round(humidity, 2),
        'pressure_inhg': round(pressure_inhg, 2),
        'dew_point_f': round(dew_point_f, 2),
        'feels_like_f': round(feels_like_f, 2),
        'wind_speed_mph': round(wind_speed_mph, 2) if wind_speed_mph else None,
        'wind_direction_degrees': wind_direction,
        'uv_index': uv_index,
        'cloud_cover_percent': cloud_cover,
        'visibility_miles': visibility_miles
    }
    logger.info(data)
    send_data(data)

if __name__ == "__main__":
    main()