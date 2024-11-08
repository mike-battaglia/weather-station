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
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 31.3,
	"longitude": -95.4,
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
	"minutely_15": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "snowfall_height", "freezing_level_height", "sunshine_duration", "weather_code", "wind_speed_10m", "wind_speed_80m", "wind_direction_10m", "wind_direction_80m", "wind_gusts_10m", "visibility", "cape", "lightning_potential", "is_day"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm", "uv_index", "uv_index_clear_sky", "is_day", "sunshine_duration", "total_column_integrated_water_vapour", "cape", "lifted_index", "convective_inhibition", "freezing_level_height", "boundary_layer_height"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timeformat": "unixtime",
	"timezone": "America/Chicago",
	"past_days": 3,
	"past_hours": 6,
	"past_minutely_15": 1,
	"forecast_days": 14,
	"forecast_hours": 24,
	"forecast_minutely_15": 96,
	"models": ["best_match", "gfs_seamless", "gfs_global", "gfs_graphcast025"]
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
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_is_day = current.Variables(3).Value()
current_precipitation = current.Variables(4).Value()
current_rain = current.Variables(5).Value()
current_showers = current.Variables(6).Value()
current_snowfall = current.Variables(7).Value()
current_weather_code = current.Variables(8).Value()
current_cloud_cover = current.Variables(9).Value()
current_pressure_msl = current.Variables(10).Value()
current_surface_pressure = current.Variables(11).Value()
current_wind_speed_10m = current.Variables(12).Value()
current_wind_direction_10m = current.Variables(13).Value()
current_wind_gusts_10m = current.Variables(14).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
print(f"Current apparent_temperature {current_apparent_temperature}")
print(f"Current is_day {current_is_day}")
print(f"Current precipitation {current_precipitation}")
print(f"Current rain {current_rain}")
print(f"Current showers {current_showers}")
print(f"Current snowfall {current_snowfall}")
print(f"Current weather_code {current_weather_code}")
print(f"Current cloud_cover {current_cloud_cover}")
print(f"Current pressure_msl {current_pressure_msl}")
print(f"Current surface_pressure {current_surface_pressure}")
print(f"Current wind_speed_10m {current_wind_speed_10m}")
print(f"Current wind_direction_10m {current_wind_direction_10m}")
print(f"Current wind_gusts_10m {current_wind_gusts_10m}")

# Process minutely_15 data. The order of variables needs to be the same as requested.
minutely_15 = response.Minutely15()
minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
minutely_15_relative_humidity_2m = minutely_15.Variables(1).ValuesAsNumpy()
minutely_15_dew_point_2m = minutely_15.Variables(2).ValuesAsNumpy()
minutely_15_apparent_temperature = minutely_15.Variables(3).ValuesAsNumpy()
minutely_15_precipitation = minutely_15.Variables(4).ValuesAsNumpy()
minutely_15_rain = minutely_15.Variables(5).ValuesAsNumpy()
minutely_15_snowfall = minutely_15.Variables(6).ValuesAsNumpy()
minutely_15_snowfall_height = minutely_15.Variables(7).ValuesAsNumpy()
minutely_15_freezing_level_height = minutely_15.Variables(8).ValuesAsNumpy()
minutely_15_sunshine_duration = minutely_15.Variables(9).ValuesAsNumpy()
minutely_15_weather_code = minutely_15.Variables(10).ValuesAsNumpy()
minutely_15_wind_speed_10m = minutely_15.Variables(11).ValuesAsNumpy()
minutely_15_wind_speed_80m = minutely_15.Variables(12).ValuesAsNumpy()
minutely_15_wind_direction_10m = minutely_15.Variables(13).ValuesAsNumpy()
minutely_15_wind_direction_80m = minutely_15.Variables(14).ValuesAsNumpy()
minutely_15_wind_gusts_10m = minutely_15.Variables(15).ValuesAsNumpy()
minutely_15_visibility = minutely_15.Variables(16).ValuesAsNumpy()
minutely_15_cape = minutely_15.Variables(17).ValuesAsNumpy()
minutely_15_lightning_potential = minutely_15.Variables(18).ValuesAsNumpy()
minutely_15_is_day = minutely_15.Variables(19).ValuesAsNumpy()

minutely_15_data = {"date": pd.date_range(
	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
	end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = minutely_15.Interval()),
	inclusive = "left"
)}
minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
minutely_15_data["relative_humidity_2m"] = minutely_15_relative_humidity_2m
minutely_15_data["dew_point_2m"] = minutely_15_dew_point_2m
minutely_15_data["apparent_temperature"] = minutely_15_apparent_temperature
minutely_15_data["precipitation"] = minutely_15_precipitation
minutely_15_data["rain"] = minutely_15_rain
minutely_15_data["snowfall"] = minutely_15_snowfall
minutely_15_data["snowfall_height"] = minutely_15_snowfall_height
minutely_15_data["freezing_level_height"] = minutely_15_freezing_level_height
minutely_15_data["sunshine_duration"] = minutely_15_sunshine_duration
minutely_15_data["weather_code"] = minutely_15_weather_code
minutely_15_data["wind_speed_10m"] = minutely_15_wind_speed_10m
minutely_15_data["wind_speed_80m"] = minutely_15_wind_speed_80m
minutely_15_data["wind_direction_10m"] = minutely_15_wind_direction_10m
minutely_15_data["wind_direction_80m"] = minutely_15_wind_direction_80m
minutely_15_data["wind_gusts_10m"] = minutely_15_wind_gusts_10m
minutely_15_data["visibility"] = minutely_15_visibility
minutely_15_data["cape"] = minutely_15_cape
minutely_15_data["lightning_potential"] = minutely_15_lightning_potential
minutely_15_data["is_day"] = minutely_15_is_day

minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
print("MINUTELY")
print(minutely_15_dataframe)

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
hourly_rain = hourly.Variables(6).ValuesAsNumpy()
hourly_showers = hourly.Variables(7).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(10).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(12).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(13).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(14).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(15).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(16).ValuesAsNumpy()
hourly_visibility = hourly.Variables(17).ValuesAsNumpy()
hourly_evapotranspiration = hourly.Variables(18).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(19).ValuesAsNumpy()
hourly_vapour_pressure_deficit = hourly.Variables(20).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(21).ValuesAsNumpy()
hourly_wind_speed_80m = hourly.Variables(22).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(23).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(24).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(25).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(26).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(27).ValuesAsNumpy()
hourly_wind_direction_180m = hourly.Variables(28).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(29).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(30).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(31).ValuesAsNumpy()
hourly_temperature_180m = hourly.Variables(32).ValuesAsNumpy()
hourly_soil_temperature_0cm = hourly.Variables(33).ValuesAsNumpy()
hourly_soil_temperature_6cm = hourly.Variables(34).ValuesAsNumpy()
hourly_soil_temperature_18cm = hourly.Variables(35).ValuesAsNumpy()
hourly_soil_temperature_54cm = hourly.Variables(36).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(37).ValuesAsNumpy()
hourly_soil_moisture_1_to_3cm = hourly.Variables(38).ValuesAsNumpy()
hourly_soil_moisture_3_to_9cm = hourly.Variables(39).ValuesAsNumpy()
hourly_soil_moisture_9_to_27cm = hourly.Variables(40).ValuesAsNumpy()
hourly_soil_moisture_27_to_81cm = hourly.Variables(41).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(42).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(43).ValuesAsNumpy()
hourly_is_day = hourly.Variables(44).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(45).ValuesAsNumpy()
hourly_total_column_integrated_water_vapour = hourly.Variables(46).ValuesAsNumpy()
hourly_cape = hourly.Variables(47).ValuesAsNumpy()
hourly_lifted_index = hourly.Variables(48).ValuesAsNumpy()
hourly_convective_inhibition = hourly.Variables(49).ValuesAsNumpy()
hourly_freezing_level_height = hourly.Variables(50).ValuesAsNumpy()
hourly_boundary_layer_height = hourly.Variables(51).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["weather_code"] = hourly_weather_code
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["visibility"] = hourly_visibility
hourly_data["evapotranspiration"] = hourly_evapotranspiration
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_80m"] = hourly_temperature_80m
hourly_data["temperature_120m"] = hourly_temperature_120m
hourly_data["temperature_180m"] = hourly_temperature_180m
hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["total_column_integrated_water_vapour"] = hourly_total_column_integrated_water_vapour
hourly_data["cape"] = hourly_cape
hourly_data["lifted_index"] = hourly_lifted_index
hourly_data["convective_inhibition"] = hourly_convective_inhibition
hourly_data["freezing_level_height"] = hourly_freezing_level_height
hourly_data["boundary_layer_height"] = hourly_boundary_layer_height

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("HOURLY")
print(hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
daily_sunrise = daily.Variables(5).ValuesAsNumpy()
daily_sunset = daily.Variables(6).ValuesAsNumpy()
daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
daily_uv_index_max = daily.Variables(9).ValuesAsNumpy()
daily_uv_index_clear_sky_max = daily.Variables(10).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
daily_showers_sum = daily.Variables(13).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(14).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(15).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(16).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(17).ValuesAsNumpy()
daily_wind_gusts_10m_max = daily.Variables(18).ValuesAsNumpy()
daily_wind_direction_10m_dominant = daily.Variables(19).ValuesAsNumpy()
daily_shortwave_radiation_sum = daily.Variables(20).ValuesAsNumpy()
daily_et0_fao_evapotranspiration = daily.Variables(21).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
daily_data["sunrise"] = daily_sunrise
daily_data["sunset"] = daily_sunset
daily_data["daylight_duration"] = daily_daylight_duration
daily_data["sunshine_duration"] = daily_sunshine_duration
daily_data["uv_index_max"] = daily_uv_index_max
daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["rain_sum"] = daily_rain_sum
daily_data["showers_sum"] = daily_showers_sum
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["precipitation_hours"] = daily_precipitation_hours
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration

daily_dataframe = pd.DataFrame(data = daily_data)
print("DAILY")
print(daily_dataframe)

#
#
#
#
#
#


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
aqi_params = {
	"latitude": 31.3,
	"longitude": -95.4,
	"current": ["us_aqi", "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "aerosol_optical_depth", "dust", "uv_index", "uv_index_clear_sky", "ammonia", "alder_pollen", "birch_pollen", "grass_pollen", "mugwort_pollen", "olive_pollen", "ragweed_pollen"],
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "carbon_dioxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "aerosol_optical_depth", "dust", "uv_index", "uv_index_clear_sky", "ammonia", "methane", "alder_pollen", "birch_pollen", "grass_pollen", "mugwort_pollen", "olive_pollen", "ragweed_pollen", "us_aqi", "us_aqi_pm2_5", "us_aqi_pm10", "us_aqi_nitrogen_dioxide", "us_aqi_carbon_monoxide", "us_aqi_ozone", "us_aqi_sulphur_dioxide"],
	"timezone": "America/Chicago",
	"past_days": 1,
	"forecast_days": 7
}
aqi_responses = openmeteo.weather_api(aqi_url, params=aqi_params)

# Process first location. Add a for-loop for multiple locations or weather models
aqi_response = aqi_responses[0]
print(f"Coordinates {aqi_response.Latitude()}°N {aqi_response.Longitude()}°E")
print(f"Elevation {aqi_response.Elevation()} m asl")
print(f"Timezone {aqi_response.Timezone()} {aqi_response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {aqi_response.UtcOffsetSeconds()} s")

# aqi_current values. The order of variables needs to be the same as requested.
aqi_current = aqi_response.Current()
aqi_current_us_aqi = aqi_current.Variables(0).Value()
aqi_current_pm10 = aqi_current.Variables(1).Value()
aqi_current_pm2_5 = aqi_current.Variables(2).Value()
aqi_current_carbon_monoxide = aqi_current.Variables(3).Value()
aqi_current_nitrogen_dioxide = aqi_current.Variables(4).Value()
aqi_current_sulphur_dioxide = aqi_current.Variables(5).Value()
aqi_current_ozone = aqi_current.Variables(6).Value()
aqi_current_aerosol_optical_depth = aqi_current.Variables(7).Value()
aqi_current_dust = aqi_current.Variables(8).Value()
aqi_current_uv_index = aqi_current.Variables(9).Value()
aqi_current_uv_index_clear_sky = aqi_current.Variables(10).Value()
aqi_current_ammonia = aqi_current.Variables(11).Value()
aqi_current_alder_pollen = aqi_current.Variables(12).Value()
aqi_current_birch_pollen = aqi_current.Variables(13).Value()
aqi_current_grass_pollen = aqi_current.Variables(14).Value()
aqi_current_mugwort_pollen = aqi_current.Variables(15).Value()
aqi_current_olive_pollen = aqi_current.Variables(16).Value()
aqi_current_ragweed_pollen = aqi_current.Variables(17).Value()

print(f"Current time {aqi_current.Time()}")
print(f"Current us_aqi {aqi_current_us_aqi}")
print(f"Current pm10 {aqi_current_pm10}")
print(f"Current pm2_5 {aqi_current_pm2_5}")
print(f"Current carbon_monoxide {aqi_current_carbon_monoxide}")
print(f"Current nitrogen_dioxide {aqi_current_nitrogen_dioxide}")
print(f"Current sulphur_dioxide {aqi_current_sulphur_dioxide}")
print(f"Current ozone {aqi_current_ozone}")
print(f"Current aerosol_optical_depth {aqi_current_aerosol_optical_depth}")
print(f"Current dust {aqi_current_dust}")
print(f"Current uv_index {aqi_current_uv_index}")
print(f"Current uv_index_clear_sky {aqi_current_uv_index_clear_sky}")
print(f"Current ammonia {aqi_current_ammonia}")
print(f"Current alder_pollen {aqi_current_alder_pollen}")
print(f"Current birch_pollen {aqi_current_birch_pollen}")
print(f"Current grass_pollen {aqi_current_grass_pollen}")
print(f"Current mugwort_pollen {aqi_current_mugwort_pollen}")
print(f"Current olive_pollen {aqi_current_olive_pollen}")
print(f"Current ragweed_pollen {aqi_current_ragweed_pollen}")

# Process hourly data. The order of variables needs to be the same as requested.
aqi_hourly= aqi_response.Hourly()
aqi_hourly_pm10 = aqi_hourly.Variables(0).ValuesAsNumpy()
aqi_hourly_pm2_5 = aqi_hourly.Variables(1).ValuesAsNumpy()
aqi_hourly_carbon_monoxide = aqi_hourly.Variables(2).ValuesAsNumpy()
aqi_hourly_carbon_dioxide = aqi_hourly.Variables(3).ValuesAsNumpy()
aqi_hourly_nitrogen_dioxide = aqi_hourly.Variables(4).ValuesAsNumpy()
aqi_hourly_sulphur_dioxide = aqi_hourly.Variables(5).ValuesAsNumpy()
aqi_hourly_ozone = aqi_hourly.Variables(6).ValuesAsNumpy()
aqi_hourly_aerosol_optical_depth = aqi_hourly.Variables(7).ValuesAsNumpy()
aqi_hourly_dust = aqi_hourly.Variables(8).ValuesAsNumpy()
aqi_hourly_uv_index = aqi_hourly.Variables(9).ValuesAsNumpy()
aqi_hourly_uv_index_clear_sky = aqi_hourly.Variables(10).ValuesAsNumpy()
aqi_hourly_ammonia = aqi_hourly.Variables(11).ValuesAsNumpy()
aqi_hourly_methane = aqi_hourly.Variables(12).ValuesAsNumpy()
aqi_hourly_alder_pollen = aqi_hourly.Variables(13).ValuesAsNumpy()
aqi_hourly_birch_pollen = aqi_hourly.Variables(14).ValuesAsNumpy()
aqi_hourly_grass_pollen = aqi_hourly.Variables(15).ValuesAsNumpy()
aqi_hourly_mugwort_pollen = aqi_hourly.Variables(16).ValuesAsNumpy()
aqi_hourly_olive_pollen = aqi_hourly.Variables(17).ValuesAsNumpy()
aqi_hourly_ragweed_pollen = aqi_hourly.Variables(18).ValuesAsNumpy()
aqi_hourly_us_aqi = aqi_hourly.Variables(19).ValuesAsNumpy()
aqi_hourly_us_aqi_pm2_5 = aqi_hourly.Variables(20).ValuesAsNumpy()
aqi_hourly_us_aqi_pm10 = aqi_hourly.Variables(21).ValuesAsNumpy()
aqi_hourly_us_aqi_nitrogen_dioxide = aqi_hourly.Variables(22).ValuesAsNumpy()
aqi_hourly_us_aqi_carbon_monoxide = aqi_hourly.Variables(23).ValuesAsNumpy()
aqi_hourly_us_aqi_ozone = aqi_hourly.Variables(24).ValuesAsNumpy()
aqi_hourly_us_aqi_sulphur_dioxide = aqi_hourly.Variables(25).ValuesAsNumpy()

aqi_hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(aqi_hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(aqi_hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = aqi_hourly.Interval()),
	inclusive = "left"
)}
aqi_hourly_data["pm10"] = aqi_hourly_pm10
aqi_hourly_data["pm2_5"] = aqi_hourly_pm2_5
aqi_hourly_data["carbon_monoxide"] = aqi_hourly_carbon_monoxide
aqi_hourly_data["carbon_dioxide"] = aqi_hourly_carbon_dioxide
aqi_hourly_data["nitrogen_dioxide"] = aqi_hourly_nitrogen_dioxide
aqi_hourly_data["sulphur_dioxide"] = aqi_hourly_sulphur_dioxide
aqi_hourly_data["ozone"] = aqi_hourly_ozone
aqi_hourly_data["aerosol_optical_depth"] = aqi_hourly_aerosol_optical_depth
aqi_hourly_data["dust"] = aqi_hourly_dust
aqi_hourly_data["uv_index"] = aqi_hourly_uv_index
aqi_hourly_data["uv_index_clear_sky"] = aqi_hourly_uv_index_clear_sky
aqi_hourly_data["ammonia"] = aqi_hourly_ammonia
aqi_hourly_data["methane"] = aqi_hourly_methane
aqi_hourly_data["alder_pollen"] = aqi_hourly_alder_pollen
aqi_hourly_data["birch_pollen"] = aqi_hourly_birch_pollen
aqi_hourly_data["grass_pollen"] = aqi_hourly_grass_pollen
aqi_hourly_data["mugwort_pollen"] = aqi_hourly_mugwort_pollen
aqi_hourly_data["olive_pollen"] = aqi_hourly_olive_pollen
aqi_hourly_data["ragweed_pollen"] = aqi_hourly_ragweed_pollen
aqi_hourly_data["us_aqi"] = aqi_hourly_us_aqi
aqi_hourly_data["us_aqi_pm2_5"] = aqi_hourly_us_aqi_pm2_5
aqi_hourly_data["us_aqi_pm10"] = aqi_hourly_us_aqi_pm10
aqi_hourly_data["us_aqi_nitrogen_dioxide"] = aqi_hourly_us_aqi_nitrogen_dioxide
aqi_hourly_data["us_aqi_carbon_monoxide"] = aqi_hourly_us_aqi_carbon_monoxide
aqi_hourly_data["us_aqi_ozone"] = aqi_hourly_us_aqi_ozone
aqi_hourly_data["us_aqi_sulphur_dioxide"] = aqi_hourly_us_aqi_sulphur_dioxide

aqi_hourly_dataframe = pd.DataFrame(data = aqi_hourly_data)
print(aqi_hourly_dataframe)

