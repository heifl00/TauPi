# Import Library
import bme280_data
import onboard_T
import math
from time import sleep

def Taupunkttemperatur(RT, rF):
    """
    Calculates the dew point temperature from the onboard temperature
    of the Pico and the humidity measured by the BME
    """
    return (237.3 * (math.log10((rF / 100 * (6.1079 * 10**((7.5 * RT) /
            (237.3 + RT))))/ 6.1078)))/(7.5
            - (math.log10((rF / 100
            * (6.1079 * 10**((7.5 * RT) / (237.3 + RT))))/ 6.1078))) 

def SchiPi():
    """
    collects the data from the Pico and BME and puts them into the dew point calculation
    function to get the corresponding dew point temperature
    
    In order to be able to give a statement about a possible mold danger, the surface temperature
    and the dew point temperature must now be compared. If the surface temperature is smaller
    than the dew point temperature, the truth value True is returned.
    """
    # data request from Pico
    RT = onboard_T.temp()
    # data request from BME280
    OT = bme280_data.bme280_temp()
    rF = bme280_data.bme280_humi()
    
    # Taupunktberechnung
    TP_temp = Taupunkttemperatur(RT, rF)
    
    return [RT, rF, OT, TP_temp, (TP_temp < OT)]
