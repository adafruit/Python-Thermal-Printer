#!/usr/bin/python

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from Yahoo! weather, prints current conditions and
# forecasts for next two days.  See timetemp.py for a different
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
# 
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import urllib, time, sys
from Adafruit_Thermal import *
from xml.dom.minidom import parseString

Station = 'NCC063'  # Durham, NC
# Station = 'OKC013'  # Norman, OK

lastUpdate   = '2015-05-26T19:34:59+00:00'

# lastUpdate is command line value (if passed)
if len(sys.argv) > 1: 
  lastUpdate = sys.argv[1]


printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch alerts from the NWS, parse resulting XML
# grw - May 26, 2015
try:
  dom = parseString(urllib.urlopen(
        'http://alerts.weather.gov/cap/wwaatmget.php?x=' + Station).read())
except:
  # printer.println('--Connection Error--')  # debugging 
  # e = sys.exc_info()[0]
  #printer.println(e)
  print(lastUpdate)
  exit(0)

# print(dom.toxml())

entries = dom.getElementsByTagName('entry')
# print('Number of entries = ', len(entries))

summaries = dom.getElementsByTagName('summary')
# print('Number of summaries = ', len(summaries))

# get the bulletin update
newUpdate = dom.getElementsByTagName('updated')[0].firstChild.data

  
if (len(summaries) > 0):
  if (newUpdate > lastUpdate):
    # print the heading    
    # print(newUpdate)
    printer.println(dom.getElementsByTagName('title')[0].firstChild.data)
    printer.feed(1)

    for entry in entries:
      # print(entry.toxml())
      eventUpdate = entry.getElementsByTagName('updated')[0].firstChild.data

      # Only print new weather events since previous bulletin
      if (eventUpdate > lastUpdate):
        event = entry.getElementsByTagName('cap:event')[0].firstChild.data
        printer.boldOn()
        printer.underlineOn()
        printer.println('{:^32}'.format(event))
        printer.underlineOff()
        printer.boldOff()

        alert = entry.getElementsByTagName('title')[0].firstChild.data
        printer.println(alert)
        printer.feed(1)
        summary  = entry.getElementsByTagName('summary')[0].firstChild.data
        printer.println(summary)
        printer.feed(2)

# output the latest update value
# printer.feed(1)
print(newUpdate)

