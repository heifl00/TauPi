# Import Library
from machine import Pin, I2C
from time import sleep
from bme280 import BME280

# Initialization I2C
i2c=I2C(0,sda=Pin(0),scl=Pin(1), freq=400000)


def i2c_device_check():
    """
    Checks if there is a connection to the BME
    """
    devices = i2c.scan()
    return not (len(devices) == 0)


## Data query ##
def bme280_temp():
    """
    Gets the temperature data from BME
    """
    bme = BME280(i2c=i2c)
    return float(bme.values[0])

def bme280_humi():
    """
    Gets the humidity data from BME
    """
    bme = BME280(i2c=i2c)
    return float(bme.values[2])
