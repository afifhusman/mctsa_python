# main.py
# ------------------------------------------
# MQTT communication and LED control
# ------------------------------------------

import machine
from machine import Pin
from time import sleep
import ubinascii
from simple import MQTTClient

# ======================================
# MQTT configuration
# ======================================
MQTT_CLUSTER_URL = b'INSERT_CLUSTER_URL'
MQTT_USER = b'INSERT_USERNAME'
MQTT_PASSWORD = b'INSERT_PASSWORD'

MQTT_SSL_PARAMS = {'server_hostname': MQTT_CLUSTER_URL}
MQTT_PORT = 0
MQTT_KEEPALIVE = 7200
MQTT_SSL = True
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# MQTT Topics
MQTT_TOPIC_TEMP_HUMID = b"mctsa/sensor"
MQTT_TOPIC_LED = b"mctsa/led"

# LED setup
led = Pin(2, Pin.OUT)

# ======================================
# MQTT functions
# ======================================

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
        print('Connected to MQTT Broker!')
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise

def subscribe(client, topic):
    client.subscribe(topic)
    print('Subscribed to topic:', topic)

def publish_mqtt(client, topic, value):
    client.publish(topic, value)
    print(f"Published {value} to topic {topic}")

def my_callback(topic, message):
    global led
    print('Received message on topic:', topic)
    print('Message:', message)
    if message == b'ON':
        led.on()
        print('LED ON')
    elif message == b'OFF':
        led.off()
        print('LED OFF')
    else:
        print('Unknown command')

# ======================================
# Main program loop
# ======================================

try:
    client = connect_mqtt()
    client.set_callback(my_callback)
    subscribe(client, MQTT_TOPIC_LED)

    while True:
        # Check for incoming MQTT messages
        client.check_msg()

        # Publish sensor data (replace "50" with actual readings)
        publish_mqtt(client, MQTT_TOPIC_TEMP_HUMID, b"50")

        sleep(2)

except Exception as e:
    print('Error:', e)
