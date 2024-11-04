import smbus2
import bme280
import requests
from datetime import datetime
import pytz
from math import log, exp

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
        feels_like_c = (hi_f - 32) * 5/9
    elif temp_c <= 10 and wind_speed_mps > 1.3:
        # Wind Chill calculation
        wc_c = 13.12 + 0.6215*temp_c - 11.37*wind_speed_mps**0.16 + 0.3965*temp_c*wind_speed_mps**0.16
        feels_like_c = wc_c
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
        'X-API-Key': 'your_pre_shared_api_key'  # Replace with your actual key
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Data sent. Server responded with: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

def main():
    temp_c, humidity, pressure, timestamp = get_sensor_data()
    dew_point = calculate_dew_point(temp_c, humidity)
    wind_speed, wind_direction, uv_index, cloud_cover, visibility = get_additional_data()

    # Convert wind speed to m/s if necessary
    if wind_speed is not None:
        wind_speed_mps = wind_speed / 3.6  # Assuming wind_speed is in km/h
    else:
        wind_speed_mps = 0

    feels_like = calculate_feels_like(temp_c, humidity, wind_speed_mps)

    data = {
        'timestamp': timestamp,
        'temperature_c': round(temp_c, 2),
        'humidity_percent': round(humidity, 2),
        'pressure_hpa': round(pressure, 2),
        'dew_point_c': round(dew_point, 2),
        'feels_like_c': round(feels_like, 2),
        'wind_speed_mps': round(wind_speed_mps, 2) if wind_speed_mps else None,
        'wind_direction_degrees': wind_direction,
        'uv_index': uv_index,
        'cloud_cover_percent': cloud_cover,
        'visibility_meters': visibility
    }
    print(data)
    send_data(data)

if __name__ == "__main__":
    main()
