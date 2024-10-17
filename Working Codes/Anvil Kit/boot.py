#############################################
# Provide your Wifi connection details here #
#############################################

WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"

#############################################

import network
from time import sleep
from machine import Pin
import ntptime

sleep(2)  # Without this, the USB handshake seems to break this script and then fail sometimes.

led = Pin(2, Pin.OUT, value=1)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to WiFi...')
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
print('Connected to WiFi:', wlan.ifconfig())

# Set the RTC to the current time

ntptime.settime()

# Solid LED means we're connected and ready to go
led.on()