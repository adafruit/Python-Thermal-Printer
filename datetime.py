#!/usr/bin/env python3

# Python3 script to print the current date and time, using
#   the Adafruit_Thermal library, in ISO 8601 format.
# https://www.iso.org/iso-8601-date-and-time-format.html

import time
from Adafruit_Thermal import *

# Lines of margin (integer)
i_feed = 3
# Seconds to pause (float)
f_pause = 1.0

# Define the printer port, speed, and timeout
printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

# Build the date stamp in the format YYYY-MM-DD ex: "2021-12-25"
datestamp = time.strftime("%Y-%m-%d", time.gmtime())
print ("Date in preferred format:", datestamp)

# Build the time stamp in the format Thh:mm:ssZ ex: "T23:59:59Z"
timestamp = 'T' + time.strftime("%H:%M:%S", time.gmtime()) + 'Z'
print ("Time in preferred format:", timestamp)

# Tell printer to sleep
printer.sleep()
# Sleep for the defined time in case we're called many times in a row
time.sleep(f_pause)
# Call wake() before printing again, even if reset
printer.wake()
# Restore printer to defaults
printer.setDefault()

# Give a little room at the top
printer.feed(i_feed)
# Center justify
printer.justify('C')
# Large size
printer.setSize('L')
# Print the date
printer.println(datestamp)
# Print the time
printer.println(timestamp)
# Give a little room at the bottom
printer.feed(i_feed)
