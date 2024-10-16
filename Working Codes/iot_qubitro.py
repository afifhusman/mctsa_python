import network
import time
from umqtt.simple import MQTTClient
import machine

# Replace with your WiFi credentials
WIFI_SSID = 'WIFI_SSID'
WIFI_PASSWORD = 'WIFI_PASSWORD'

# Qubitro MQTT settings
MQTT_BROKER = 'broker.qubitro.com'
MQTT_PORT = 1883  # Use 8883 for SSL
DEVICE_ID = 'XXX'
DEVICE_TOKEN = 'XXX'  # Replace with your Qubitro device token
MQTT_TOPIC = 'XXX'  # Replace with your specific topic

# Function to connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to WiFi:', wlan.ifconfig())

# Function to send MQTT data
def send_mqtt_data(client, data):
    try:
        print(f"Publishing to {MQTT_TOPIC}: {data}")
        client.publish(MQTT_TOPIC, data)
        print("Data sent successfully")
    except Exception as e:
        print("Failed to send data:", e)

# Setup MQTT client
def setup_mqtt():
    client = MQTTClient(DEVICE_ID, MQTT_BROKER, port=MQTT_PORT, user=DEVICE_ID, password=DEVICE_TOKEN, keepalive=60)
    return client

# Main function
def main():
    # Connect to WiFi
    connect_to_wifi()

    # Setup MQTT client
    client = setup_mqtt()
    
    # Connect to the MQTT broker
    print("Connecting to MQTT broker...")
    try:
        client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)
        return

    # Example payload (JSON format)
    payload = '{"temperature": 23.5, "humidity": 60}'

    # Send the payload to the MQTT broker
    send_mqtt_data(client, payload)
    
    # Disconnect after sending the message
    client.disconnect()
    
if __name__ == '__main__':
    main()
    
