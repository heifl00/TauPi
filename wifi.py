import network
import secrets
import time
from machine import Pin
from time import sleep

def connect():
    """
    Creates a Wi-Fi connection
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    led = Pin("LED", Pin.OUT)
    
    while wlan.isconnected() == False:
        print('Connecting...')
        led.toggle()
        sleep(0.5)
    
    print('Connected')
    print(wlan.ifconfig())
    
def is_connected():
    """
    Checks if there is a Wi-Fi connection
    """
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()