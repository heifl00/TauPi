# Import Library
from machine import Pin, I2C
import time
import network
import ubot
import secrets
import bme280_data
import taupunktberechnung
import onboard_T
import wifi
import uasyncio as asyncio

##########################################################################################################

# global variables
telegram_api_key = "5876295566:AAEIo9IDt8u4TkzVWcfIPLB-w3951lbVde4"

led = Pin("LED", Pin.OUT)

print_auto_values = False

##########################################################################################################
# send a message without a message from the user
def message_without_call(userchatid, text):
    bot.send(userchatid, text)
    
# welcome message
def welcome_message():
    userchatid = secrets.userchatid
    welcome = ("<pre>Hallo! Hier ist der Bot-TauPi! Hier findest du die Uebersicht über alle Befehle zur Steuerung von TauPi: </pre> \n"
               "<pre>----------------------------\n"
               "   --Einmalige Abfragen-- \n"
               "----------------------------</pre>\n"
               "<pre> - zeigt beim benutzen eines Befehls einmalig die gewuenschten Werte des Schimmelwaechters an.</pre> \n"
               "/bme <pre> = zeigt alle Werte des BME280 an</pre> \n"
               "/temp <pre> = zeigt die Oberflaechentemperatur an</pre> \n"
               "/humi <pre> = zeigt die rel. Luftfeuchtigkeit an</pre> \n"
               "<pre>----------------------------\n"
               " --Automatische Abfragen--\n"
               "----------------------------</pre>\n"
               "<pre> - zeigt bei eingeschalteter Funktion kontinuierlich alle Werte des Schimmelwaechters an</pre> \n"
               "/auto_on <pre> = schaltet die automatischen Ausgabe an</pre> \n"
               "/auto_off <pre> = schaltet die automatischen Ausgabe ab</pre> \n")
    message_without_call(userchatid, welcome)
    
# auto send message when bme is not available
def bme_available():
    userchatid = secrets.userchatid
       
    if not bme280_data.i2c_device_check():
        text = 'Keine Verbindung zum BME280.'
        message_without_call(userchatid, text)
        return False
    else:
        return True

# SchiPi
def SchiPi_Warnung():
    print('Schimmelwächter on')
    result = taupunktberechnung.SchiPi()
    print(result)
    userchatid = secrets.userchatid
    
    if result[4] == True:
        text = ('Es besteht keine Schimmelgefahr die Ergebnisse sehen wie folgt aus: ' + '\n')
    else:
        text = ('Es besteht Schimmelgefahr die Ergebnisse sehen wie folgt aus:' + '\n')

    result_text = ("Oberflächentemperatur: {:<10.2f} &#176;C\n"
                   "rel. Luftfeuchte:      {:<10.1f} %\n"
                   "Raumtemperatur:        {:<10.5f} &#176;C\n"
                   "Taupunkttemperatur:    {:<10.5f} &#176;C\n").format(result[2], result[1], result[0], result[3])
    # style the text to code block text
    code_block_text = "<pre>" + text + result_text + "</pre>"
    message_without_call(userchatid, code_block_text)
    
##########################################################################################################
# send a message as an answer
# Telegram default callback
def get_message(message):
    text = ('<pre>TauPi kann mit dieser Nachricht nichts anfangen. Beim klicken auf Menu findest du alle vorhandenen Befehle.</pre>')
    bot.reply_to(message['message']['chat']['id'], text, message['message']['message_id'])

# send PONG text as ping reply
def reply_ping(message):
    text = 'pong'
    bot.send(message['message']['chat']['id'], text)

# send an overview of all commands
def overview(message):
    welcome = ("<pre>Hier findest du die Uebersicht über alle Befehle zur Steuerung von TauPi: </pre> \n"
               "<pre>----------------------------\n"
               "   --Einmalige Abfragen-- \n"
               "----------------------------</pre>\n"
               "<pre> - zeigt beim benutzen eines Befehls einmalig die gewuenschten Werte des Schimmelwaechters an.</pre> \n"
               "/bme <pre> = zeigt alle Werte des BME280 an</pre> \n"
               "/temp <pre> = zeigt die Oberflaechentemperatur an</pre> \n"
               "/humi <pre> = zeigt die rel. Luftfeuchtigkeit an</pre> \n"
               "<pre>----------------------------\n"
               " --Automatische Abfragen--\n"
               "----------------------------</pre>\n"
               "<pre> - zeigt bei eingeschalteter Funktion kontinuierlich alle Werte des Schimmelwaechters an</pre> \n"
               "/auto_on <pre> = schaltet die automatischen Ausgabe an</pre> \n"
               "/auto_off <pre> = schaltet die automatischen Ausgabe ab</pre> \n")
    bot.send(message['message']['chat']['id'], welcome)

# send all values as answer
def bme280_all_values(message):
    temp = bme280_data.bme280_temp()
    humi = bme280_data.bme280_humi()
    text = ("<pre>Oberflächentemperatur:   {:<5.2f} &#176;C\n"
            "rel. Luftfeuchtigkeit:   {:<5.2f} %</pre>").format(temp, humi)
    bot.send(message['message']['chat']['id'], text)

# send temp value as answer
def bme280_temp(message):
    temp = bme280_data.bme280_temp()
    text = ("<pre>Oberflächentemperatur:   {:<5.2f} &#176;C</pre>").format(temp)
    bot.send(message['message']['chat']['id'], text)

# send humi value as answer
def bme280_humi(message):
    humi = bme280_data.bme280_humi()
    text = ("<pre>rel. Luftfeuchtigkeit:   {:<5.2f} %</pre>").format(humi)
    bot.send(message['message']['chat']['id'], text)
    
# auto send values on (print_auto_values = True)
def auto_values_on(message):
    bot.send(message['message']['chat']['id'], '<pre>Es werden ab jetzt immer automatisch die aktuellen Daten angezeigt.' + '\n' +
    'Möchtest du das beenden benutze den Befehl </pre>/auto_off.')
    global print_auto_values
    print_auto_values = True    

# auto send values off (print_auto_values = False)
def auto_values_off(message):
    bot.send(message['message']['chat']['id'], '<pre>Es werden ab jetzt keine aktuellen Daten mehr automatisch angezeigt.' + '\n' +
    'Möchtest du automatisch dir die aktuellen Daten anzeigen lassen, benutze den Befehl </pre>/auto_on.')
    global print_auto_values
    print_auto_values = False

##########################################################################################################

# WLAN
wifi.connect()

# start telegram bot
bot = ubot.ubot(telegram_api_key)
print('Bot ist da!')

# Welcome message from Bot
welcome_message()

# register handler-functions
# Register the 'reply_ping' function to be called when '/ping' command is received
bot.register('/ping', reply_ping)
# Register the 'overview' function to be called when '/overview' command is received
bot.register('/overview', overview)

# Register the 'bme280_all_values' function to be called when '/bme' command is received
bot.register('/bme', bme280_all_values)
# Register the 'bme280_temp' function to be called when '/temp' command is received
bot.register('/temp', bme280_temp)
# Register the 'bme280_humi' function to be called when '/humi' command is received
bot.register('/humi', bme280_humi)

# Register the 'auto_values_on' function to be called when '/auto_on' command is received
bot.register('/auto_on', auto_values_on)
# Register the 'auto_values_off' function to be called when '/auto_off' command is received
bot.register('/auto_off', auto_values_off)

# Register the 'get_message' function to be called
# for all other messages that do not match any registered command
bot.set_default_handler(get_message)


# --- main loop ---
while True:
    print('...................')
    
    if not wifi.is_connected():
        print('Wi-Fi not available! Trying to connect...')
        wifi.connect()
        continue # with next loop iteration.
      

    if not bme_available():
        print('BME not available! Please check connection.')
        continue # with next loop iteration.
    
    print('Bot parse message.')
    part = bot.read_once()
         
    if print_auto_values: # ist das gleiche wie: print_auto_values == True:
        SchiPi_Warnung()
        
    time.sleep(2)
