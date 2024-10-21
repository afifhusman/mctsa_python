import network

# WiFi configuration
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD= "WIFI_PASSWORD"

def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Connecting to WiFi...')
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            pass
    print('Connection successful!')
    network_info = wifi.ifconfig()
    print('IP address:', network_info[0])
    
connect_to_wifi()