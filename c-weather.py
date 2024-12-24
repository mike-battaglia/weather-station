import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the BME280
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Optional: Change the sea-level pressure to match your location for accurate altitude
# bme280.sea_level_pressure = 1013.25  # Default sea-level pressure in hPa

# Read and print sensor data
temperature = bme280.temperature
humidity = bme280.humidity
pressure = bme280.pressure

print(f"Temperature: {temperature:.2f} °C")
print(f"Humidity: {humidity:.2f} %")
print(f"Pressure: {pressure:.2f} hPa")
