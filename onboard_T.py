# Import Library
from machine import ADC , Pin

def temp():
    """
    Gets the onboard temperature data from the pico
    """
    ad_read = ADC(4)
    temp_value = ad_read.read_u16()
    temp_resolution = 3.3/65535
    temp_voltage = temp_value * temp_resolution
    
    temp = 27 - (temp_voltage - 0.706)/0.001721
    
    return temp