# Adapted from Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-w-mqtt-micropython/


import machine
from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient
import ubinascii

#======================================
# WiFi configuration
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD= "WIFI_PASSWORD"

# HiveMQ Cloud MQTT configuration
MQTT_CLUSTER_URL = b'INSERT_CLUSTER_URL'  #
MQTT_USER = b'INSERT_USERNAME'
MQTT_PASSWORD = b'INSERT_PASSWORD'
#=======================================

MQTT_SSL_PARAMS = {'server_hostname': MQTT_CLUSTER_URL}
MQTT_PORT = 0
MQTT_KEEPALIVE = 7200
MQTT_SSL = True 
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID based on ESP32's MAC address

#MQTT Topics
MQTT_TOPIC_TEMP_HUMID = "mctsa/sensor"
MQTT_TOPIC_LED = "mctsa/led"

#led
led = Pin(2, Pin.OUT)

def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_CLUSTER_URL,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,
                            ssl=MQTT_SSL,
                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback
    
# Subcribe to MQTT topics
def subscribe(client, topic):
    client.subscribe(topic)
    print('Subscribed to topic:', topic)
          
def publish_mqtt(topic, value):
    client.publish(topic, value)
    print(f"Published {value} to topic {topic}")

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

def my_callback(topic, message):
    # Perform desired actions based on the subscribed topic and response
    global led
    print('Received message on topic:', topic)
    print('Response:', message)
    # Check the content of the received message
    if message == b'ON':
        print('Turning LED ON')
        led.on()  # Turn LED ON
    elif message == b'OFF':
        print('Turning LED OFF')
        led.off()  # Turn LED OFF
    else:
        print('Unknown command')

# program start here 

try:
    connect_to_wifi()
    # Connect to MQTT broker, start MQTT client
    client = connect_mqtt()
    
    client.set_callback(my_callback)
    subscribe(client, MQTT_TOPIC_LED)
    while True:
        # Read sensor data
        #temperature, humidity, pressure = get_sensor_readings()
        
        client.check_msg()
        
        # Publish as MQTT payload
        publish_mqtt(MQTT_TOPIC_TEMP_HUMID, "50")

        # Delay 10 seconds
        sleep(2)

except Exception as e:
    print('Error:', e)
