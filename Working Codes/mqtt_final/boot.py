# boot.py
# ------------------------------------------
# Handles Wi-Fi connection at startup
# ------------------------------------------

import network
from time import sleep

# WiFi configuration
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"

def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Connecting to WiFi...')
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            sleep(0.5)
            print('.', end='')
    print('\nConnection successful!')
    print('IP address:', wifi.ifconfig()[0])

# Run WiFi connection at boot
connect_to_wifi()
