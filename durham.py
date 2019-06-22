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

Station = 'NCC063'
# Station = 'OKC013'

lastUpdate  = '2015-05-26T19:34:59+00:00'
newUpdate   = '2015-05-26T19:34:59+00:00'
eventUpdate = '2015-05-26T19:34:59+00:00'

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch alerts from the NWS, parse resulting XML
# grw - May 26, 2015
try:
  dom = parseString(urllib.urlopen(
        'http://alerts.weather.gov/cap/wwaatmget.php?x=' + Station).read())

  print(dom.toxml())

# # Print current conditions
# printer.boldOn()
# printer.print('{:^32}'.format('Current conditions:'))
# printer.boldOff()
# printer.print('{:^32}'.format(
#  dom.getElementsByTagName('pubDate')[0].firstChild.data))

  entries = dom.getElementsByTagName('entry')
  print('Number of entries = ', len(entries))

  summaries = dom.getElementsByTagName('summary')
  print('Number of summaries = ', len(summaries))

  newUpdate = dom.getElementsByTagName('updated')[0].firstChild.data

  
  if (len(summaries) > 0):
    if (newUpdate > lastUpdate):
      # print the heading    
      print(dom.getElementsByTagName('updated')[0].firstChild.data)
      print(dom.getElementsByTagName('title')[0].firstChild.data)
      print

      for entry in entries:
        # print(entry.toxml())
        eventUpdate = entry.getElementsByTagName('updated')[0].firstChild.data

        # Only print new weather events
        if (eventUpdate > lastUpdate):
          event = entry.getElementsByTagName('cap:event')[0].firstChild.data
          print(event) 
          alert = entry.getElementsByTagName('title')[0].firstChild.data
          print(alert)
          print
          summary  = entry.getElementsByTagName('summary')[0].firstChild.data
          print(summary)
          print
  # output the latest update value
  print(newUpdate)
except:
  print('--Connection Error--')  # debugging 
  e = sys.exc_info()[0]
  print(e)
  exit(0)

# cond = dom.getElementsByTagName('yweather:condition')[0].getAttribute('text')
# printer.print(temp)
# printer.print(deg)
# printer.println(' ' + cond)
# printer.boldOn()

