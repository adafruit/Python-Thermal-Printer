#!/usr/bin/python3
# pylint: disable=E1101,W0614

import time
from Adafruit_Thermal import *

i_feed = 3
f_pause = 1.0

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

datestamp = time.strftime("%Y-%m-%d", time.gmtime())
print ("Date in preferred format:", datestamp)
timestamp = 'T' + time.strftime("%H:%M:%S", time.gmtime()) + 'Z'
print ("Time in preferred format:", timestamp)

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

# Tell printer to sleep
printer.sleep()
# Call wake() before printing again, even if reset
printer.wake()
# Restore printer to defaults
printer.setDefault()

# Sleep for one second in case we're called many times
time.sleep(f_pause)
