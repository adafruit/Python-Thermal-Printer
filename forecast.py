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
import urllib, time
import ConfigParser
from Adafruit_Thermal import *
from xml.dom.minidom import parseString

# WOEID indicates the geographic location for the forecast.  It is
# not a ZIP code or other common indicator.  Instead, it can be found
# by 'manually' visiting http://weather.yahoo.com, entering a location
# and requesting a forecast, then copy the number from the end of the
# current URL string and paste it here.
# (note that this value has moved to the config file)

# Dumps one forecast line to the printer
def forecast(idx):
	tag     = 'yweather:forecast'
	day     = dom.getElementsByTagName(tag)[idx].getAttribute('day')
	lo      = dom.getElementsByTagName(tag)[idx].getAttribute('low')
	hi      = dom.getElementsByTagName(tag)[idx].getAttribute('high')
	cond    = dom.getElementsByTagName(tag)[idx].getAttribute('text')
	printer.print(day + ': low ' + lo )
	printer.print(deg)
	printer.print(' high ' + hi)
	printer.print(deg)
	printer.println(' ' + cond)

config = ConfigParser.SafeConfigParser({'woeid': '2459115'}) # Default to NYC
config.read('options.cfg')
woeid = config.get('forecast', 'woeid')

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch forecast data from Yahoo!, parse resulting XML
dom = parseString(urllib.urlopen(
        'http://weather.yahooapis.com/forecastrss?w=' + woeid).read())

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format(
  dom.getElementsByTagName('description')[0].firstChild.data))
printer.inverseOff()

# Print current conditions
printer.boldOn()
printer.print('{:^32}'.format('Current conditions:'))
printer.boldOff()
printer.print('{:^32}'.format(
  dom.getElementsByTagName('pubDate')[0].firstChild.data))
temp = dom.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
cond = dom.getElementsByTagName('yweather:condition')[0].getAttribute('text')
printer.print(temp)
printer.print(deg)
printer.println(' ' + cond)
printer.boldOn()

# Print forecast
printer.print('{:^32}'.format('Forecast:'))
printer.boldOff()
forecast(0)
forecast(1)

printer.feed(3)
