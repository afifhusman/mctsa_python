import modules.anvil.esp32 as anvil
import uasyncio as a
import time
import machine
import network

# This is an example Anvil Uplink script for the ESP32.

UPLINK_KEY = "YOUR_ANVIL_SERVER_UPLINK_KEY"

# Set Onboard LED.
led = machine.Pin(2, machine.Pin.OUT, value=1)


# Call the following function from your Anvil app:
#
#    anvil.server.call('pico_fn', 42)
#
        
@anvil.callable(is_async=True)
async def pico_fn(n):
    # Output will go to the Pico W serial port
    print(f"Called local function with argument: {n}")

    # Blink the LED and then double the argument and return it.
    for i in range(10):
        led.value(not bool(led.value()))
        await a.sleep_ms(50)
    return n * 2

# Connect the Anvil Uplink. In MicroPython, this call will block forever.

anvil.connect(UPLINK_KEY)