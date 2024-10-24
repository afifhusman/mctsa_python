## Display the next prayer time on 16x2 LCD. Uses API created and maintained by Zaim Ramlan [https://github.com/zaimramlan/waktu-solat-api]
## for this example, install the i2c library first. type the following in thonny shell, press enter after each command.
## connect your esp32 to internet first. refer wifi sample code.
## >>> import mip
## >>> mip.install("github:brainelectronics/micropython-i2c-lcd")

from lcd_i2c import LCD
from machine import I2C, Pin

# PCF8574 on 0x50
I2C_ADDR = 0x3f    #esp32 wroom i2c address
NUM_ROWS = 2
NUM_COLS = 16

# define custom I2C interface, default is 'I2C(0)'
# check the docs of your device for further details and pin infos
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=800000)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)
lcd.begin()
#lcd.cursor_position = (0, 1)
from time import sleep

import urequests
import ujson
import utime

# API URL
url = "https://waktu-solat-api.herokuapp.com/api/v1/prayer_times.json?negeri=selangor&zon=gombak"

# Helper function to convert time string to seconds since midnight
def time_to_seconds(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 3600 + m * 60

# Function to get current time in seconds since midnight adjusted for GMT+8
def get_current_time():
    # Get the current UTC time (year, month, day, hour, min, sec, weekday, yearday)
    current_time = utime.localtime()

    # Add 8 hours to adjust for GMT+8
    gmt_offset = 8 * 3600
    adjusted_time = utime.mktime(current_time) + gmt_offset  # Convert to seconds since epoch and adjust

    # Convert adjusted time back to struct_time in local GMT+8
    local_time = utime.localtime(adjusted_time)

    # Return the time in seconds since midnight
    return local_time[3] * 3600 + local_time[4] * 60 + local_time[5]  # Convert hours, minutes, seconds to seconds since midnight

# Function to fetch prayer times and find the nearest time
def check_prayer_times():
    # Send GET request to the API
    response = urequests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = ujson.loads(response.text)
        
        # Get the current time adjusted for GMT+8
        current_time_sec = get_current_time()

        # List to store prayer times in seconds since midnight
        prayer_times = []

        # Extract prayer times and convert to seconds since midnight
        for waktu in data['data']['zon'][0]['waktu_solat']:
            prayer_times.append((waktu['name'], time_to_seconds(waktu['time'])))

        # Find the nearest prayer time after the current time
        nearest_time = None
        nearest_name = None
        for name, prayer_time_sec in prayer_times:
            if prayer_time_sec > current_time_sec:
                if nearest_time is None or prayer_time_sec < nearest_time:
                    nearest_time = prayer_time_sec
                    nearest_name = name
        
        # Output the nearest prayer time
        if nearest_time is not None:
            # Convert the nearest time back to hours and minutes
            nearest_hour = nearest_time // 3600
            nearest_minute = (nearest_time % 3600) // 60
            lcd.clear()
            lcd.print(f"Next prayer:")
            lcd. set_cursor(0,1)
            lcd.print(f"{nearest_name} at {nearest_hour:02d}:{nearest_minute:02d}")
        else:
            lcd.print("Error getting prayer time")


    # Close the response
    response.close()

# Run the check every 5 minutes
while True:
    check_prayer_times()
    utime.sleep(300)  # Wait for 5 minutes before checking again
