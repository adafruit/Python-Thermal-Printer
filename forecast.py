#!/usr/bin/python

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from DarkSky.net's API, prints current conditions and
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
from Adafruit_Thermal import *
from datetime import date
from datetime import datetime
import calendar
import urllib, json

API_KEY = "YOUR_API_KEY"

LAT = "40.726019"
LONG = "-74.00536"

# Dumps one forecast line to the printer
def forecast(idx):

    date = datetime.fromtimestamp(int(data['daily']['data'][idx]['time']))

    day     = calendar.day_name[date.weekday()]
    lo      = data['daily']['data'][idx]['temperatureMin']
    hi      = data['daily']['data'][idx]['temperatureMax']
    cond    = data['daily']['data'][idx]['summary']
    printer.print(day + ': low ' + str(lo) )
    printer.print(deg)
    printer.print(' high ' + str(hi))
    printer.print(deg)
    printer.println(' ' + cond.replace(u'\u2013', '-').encode('utf-8')) # take care of pesky unicode dash

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

url = "https://api.darksky.net/forecast/"+API_KEY+"/"+LAT+","+LONG+"?exclude=[alerts,minutely,hourly,flags]&units=us"
response = urllib.urlopen(url)
data = json.loads(response.read())

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format("DarkSky.Net Forecast"))
printer.inverseOff()

# Print current conditions
printer.boldOn()
printer.print('{:^32}'.format('Current conditions:'))
printer.boldOff()


temp = data['currently']['temperature']
cond = data['currently']['summary']
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
