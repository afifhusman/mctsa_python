import network
import time
from umqtt.simple import MQTTClient
import machine
import dht

# Replace with your WiFi credentials
WIFI_SSID = 'WIFI_SSID'
WIFI_PASSWORD = 'WIFI_PASSWORD'

# Qubitro MQTT settings
MQTT_BROKER = 'broker.qubitro.com'
MQTT_PORT = 1883  # Use 8883 for SSL
DEVICE_ID = 'XXX'
DEVICE_TOKEN = 'XXX'  # Replace with your Qubitro device token
MQTT_TOPIC = 'XXX'  # Replace with your specific topic


#Set up DHT11 sensor
DHT_PIN = machine.Pin(23)  #
dht_sensor = dht.DHT11(DHT_PIN)

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

# Function to read data from DHT11 sensor
def read_dht11():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f'Temperature: {temperature}°C, Humidity: {humidity}%')
        return temperature, humidity
    except OSError as e:
        print("Failed to read from DHT sensor:", e)
        return None, None

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

    while True:
        # Read temperature and humidity from DHT11 sensor
        temperature, humidity = read_dht11()
        
        if temperature is not None and humidity is not None:
            # Format payload as JSON
            payload = '{"temperature": %s, "humidity": %s}' % (temperature, humidity)
            
            # Send the payload to the MQTT broker
            send_mqtt_data(client, payload)
        else:
            print("Skipping MQTT publish due to sensor error")

        # Wait for a while before sending the next data (e.g., every 2 seconds)
        time.sleep(525)
    
if __name__ == '__main__':
    main()
    
