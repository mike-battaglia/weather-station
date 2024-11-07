import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 31.3173151,
	"longitude": -95.4564265,
	"current": ["us_aqi", "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "aerosol_optical_depth", "dust", "uv_index", "uv_index_clear_sky", "ammonia", "alder_pollen", "birch_pollen", "grass_pollen", "mugwort_pollen", "olive_pollen", "ragweed_pollen"],
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "aerosol_optical_depth", "dust", "uv_index", "uv_index_clear_sky", "ammonia", "methane", "alder_pollen", "birch_pollen", "grass_pollen", "mugwort_pollen", "olive_pollen", "ragweed_pollen", "us_aqi", "us_aqi_pm2_5", "us_aqi_pm10", "us_aqi_nitrogen_dioxide", "us_aqi_carbon_monoxide", "us_aqi_ozone", "us_aqi_sulphur_dioxide"],
	"timeformat": "unixtime",
	"timezone": "America/Chicago",
	"past_days": 3,
	"forecast_days": 7
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_us_aqi = current.Variables(0).Value()
current_pm10 = current.Variables(1).Value()
current_pm2_5 = current.Variables(2).Value()
current_carbon_monoxide = current.Variables(3).Value()
current_nitrogen_dioxide = current.Variables(4).Value()
current_sulphur_dioxide = current.Variables(5).Value()
current_ozone = current.Variables(6).Value()
current_aerosol_optical_depth = current.Variables(7).Value()
current_dust = current.Variables(8).Value()
current_uv_index = current.Variables(9).Value()
current_uv_index_clear_sky = current.Variables(10).Value()
current_ammonia = current.Variables(11).Value()
current_alder_pollen = current.Variables(12).Value()
current_birch_pollen = current.Variables(13).Value()
current_grass_pollen = current.Variables(14).Value()
current_mugwort_pollen = current.Variables(15).Value()
current_olive_pollen = current.Variables(16).Value()
current_ragweed_pollen = current.Variables(17).Value()

print(f"Current time {current.Time()}")
print(f"Current us_aqi {current_us_aqi}")
print(f"Current pm10 {current_pm10}")
print(f"Current pm2_5 {current_pm2_5}")
print(f"Current carbon_monoxide {current_carbon_monoxide}")
print(f"Current nitrogen_dioxide {current_nitrogen_dioxide}")
print(f"Current sulphur_dioxide {current_sulphur_dioxide}")
print(f"Current ozone {current_ozone}")
print(f"Current aerosol_optical_depth {current_aerosol_optical_depth}")
print(f"Current dust {current_dust}")
print(f"Current uv_index {current_uv_index}")
print(f"Current uv_index_clear_sky {current_uv_index_clear_sky}")
print(f"Current ammonia {current_ammonia}")
print(f"Current alder_pollen {current_alder_pollen}")
print(f"Current birch_pollen {current_birch_pollen}")
print(f"Current grass_pollen {current_grass_pollen}")
print(f"Current mugwort_pollen {current_mugwort_pollen}")
print(f"Current olive_pollen {current_olive_pollen}")
print(f"Current ragweed_pollen {current_ragweed_pollen}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
hourly_carbon_dioxide = hourly.Variables(3).ValuesAsNumpy()
hourly_nitrogen_dioxide = hourly.Variables(4).ValuesAsNumpy()
hourly_sulphur_dioxide = hourly.Variables(5).ValuesAsNumpy()
hourly_ozone = hourly.Variables(6).ValuesAsNumpy()
hourly_aerosol_optical_depth = hourly.Variables(7).ValuesAsNumpy()
hourly_dust = hourly.Variables(8).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(9).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(10).ValuesAsNumpy()
hourly_ammonia = hourly.Variables(11).ValuesAsNumpy()
hourly_methane = hourly.Variables(12).ValuesAsNumpy()
hourly_alder_pollen = hourly.Variables(13).ValuesAsNumpy()
hourly_birch_pollen = hourly.Variables(14).ValuesAsNumpy()
hourly_grass_pollen = hourly.Variables(15).ValuesAsNumpy()
hourly_mugwort_pollen = hourly.Variables(16).ValuesAsNumpy()
hourly_olive_pollen = hourly.Variables(17).ValuesAsNumpy()
hourly_ragweed_pollen = hourly.Variables(18).ValuesAsNumpy()
hourly_us_aqi = hourly.Variables(19).ValuesAsNumpy()
hourly_us_aqi_pm2_5 = hourly.Variables(20).ValuesAsNumpy()
hourly_us_aqi_pm10 = hourly.Variables(21).ValuesAsNumpy()
hourly_us_aqi_nitrogen_dioxide = hourly.Variables(22).ValuesAsNumpy()
hourly_us_aqi_carbon_monoxide = hourly.Variables(23).ValuesAsNumpy()
hourly_us_aqi_ozone = hourly.Variables(24).ValuesAsNumpy()
hourly_us_aqi_sulphur_dioxide = hourly.Variables(25).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["pm10"] = hourly_pm10
hourly_data["pm2_5"] = hourly_pm2_5
hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
hourly_data["carbon_dioxide"] = hourly_carbon_dioxide
hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
hourly_data["ozone"] = hourly_ozone
hourly_data["aerosol_optical_depth"] = hourly_aerosol_optical_depth
hourly_data["dust"] = hourly_dust
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["ammonia"] = hourly_ammonia
hourly_data["methane"] = hourly_methane
hourly_data["alder_pollen"] = hourly_alder_pollen
hourly_data["birch_pollen"] = hourly_birch_pollen
hourly_data["grass_pollen"] = hourly_grass_pollen
hourly_data["mugwort_pollen"] = hourly_mugwort_pollen
hourly_data["olive_pollen"] = hourly_olive_pollen
hourly_data["ragweed_pollen"] = hourly_ragweed_pollen
hourly_data["us_aqi"] = hourly_us_aqi
hourly_data["us_aqi_pm2_5"] = hourly_us_aqi_pm2_5
hourly_data["us_aqi_pm10"] = hourly_us_aqi_pm10
hourly_data["us_aqi_nitrogen_dioxide"] = hourly_us_aqi_nitrogen_dioxide
hourly_data["us_aqi_carbon_monoxide"] = hourly_us_aqi_carbon_monoxide
hourly_data["us_aqi_ozone"] = hourly_us_aqi_ozone
hourly_data["us_aqi_sulphur_dioxide"] = hourly_us_aqi_sulphur_dioxide

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
