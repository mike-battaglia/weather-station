import smbus2
import bme280
import requests
from datetime import datetime
import pytz
from math import log, exp
import os

# Get the API key from environment variables
api_key = os.getenv('WEATHER_API_KEY')

# Sensor settings
port = 1
address = 0x77  # Change to 0x77 if your sensor uses that address
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# Timezone settings
timezone = pytz.timezone('America/Chicago')

def get_sensor_data():
    data = bme280.sample(bus, address, calibration_params)
    temp_c = data.temperature
    humidity = data.humidity
    pressure = data.pressure
    timestamp = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    return temp_c, humidity, pressure, timestamp

def calculate_dew_point(temp_c, humidity):
    # Dew Point calculation using Magnus formula
    b = 17.62
    c = 243.12
    gamma = (b * temp_c / (c + temp_c)) + log(humidity / 100.0)
    dew_point = (c * gamma) / (b - gamma)
    return dew_point

def calculate_feels_like(temp_c, humidity, wind_speed_mps):
    temp_f = temp_c * 9/5 + 32
    wind_speed_mph = wind_speed_mps * 2.23694

    # Determine which formula to use
    if temp_f >= 80 and humidity >= 40:
        # Heat Index calculation
        hi_f = -42.379 + 2.04901523*temp_f + 10.14333127*humidity
        hi_f += -0.22475541*temp_f*humidity - 6.83783e-3*temp_f**2
        hi_f += -5.481717e-2*humidity**2 + 1.22874e-3*temp_f**2*humidity
        hi_f += 8.5282e-4*temp_f*humidity**2 - 1.99e-6*temp_f**2*humidity**2
        feels_like_f = hi_f
    elif temp_c <= 10 and wind_speed_mps > 1.3:
        # Wind Chill calculation
        wc_f = 35.74 + 0.6215*temp_f - 35.75*wind_speed_mph**0.16 + 0.4275*temp_f*wind_speed_mph**0.16
        feels_like_f = wc_f
    else:
        # Apparent Temperature calculation
        e = humidity / 100 * 6.105 * exp(17.27 * temp_c / (237.7 + temp_c))
        feels_like_c = temp_c + 0.33 * e - 0.70 * wind_speed_mps - 4.00
        feels_like_f = feels_like_c * 9/5 + 32

    return feels_like_f

def get_additional_data():
    # Free API: Open-Meteo
    api_url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=31.3256&longitude=-95.3677&current_weather=true&"
        "hourly=cloudcover,visibility"
    )
    try:
        response = requests.get(api_url)
        data = response.json()
        current_weather = data.get('current_weather', {})
        wind_speed = current_weather.get('windspeed')
        wind_direction = current_weather.get('winddirection')
        cloud_cover = data.get('hourly', {}).get('cloudcover', [None])[0]
        visibility = data.get('hourly', {}).get('visibility', [None])[0]
        uv_index = data.get('hourly', {}).get('uv_index', [None])[0]
        return wind_speed, wind_direction, uv_index, cloud_cover, visibility
    except Exception as e:
        print(f"Error fetching additional data: {e}")
        return None, None, None, None, None

def send_data(data):
    url = 'https://garyweather.com/wp-json/custom/v1/weather'
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key  # Use the API key defined above
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Data sent. Server responded with: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

def main():
    temp_c, humidity, pressure, timestamp = get_sensor_data()
    dew_point_c = calculate_dew_point(temp_c, humidity)
    wind_speed, wind_direction, uv_index, cloud_cover, visibility = get_additional_data()

    # Convert units to imperial
    temp_f = temp_c * 9/5 + 32
    pressure_inhg = pressure * 0.02953  # Convert hPa to inHg
    dew_point_f = dew_point_c * 9/5 + 32
    wind_speed_mph = wind_speed / 1.609 if wind_speed is not None else 0  # Assuming wind_speed is in km/h
    visibility_miles = visibility * 0.000621371 if visibility is not None else None  # Convert meters to miles

    feels_like_f = calculate_feels_like(temp_c, humidity, wind_speed_mph / 2.23694)  # Convert mph back to m/s for calculation

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
    print(data)
    send_data(data)

if __name__ == "__main__":
    main()
