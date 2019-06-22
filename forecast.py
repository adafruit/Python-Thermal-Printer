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
import urllib, time, json, math
from Adafruit_Thermal import *

# LOCID indicates the geographic location for the forecast.  It is
# not a ZIP code or other common indicator.  Instead, it can be found
# by 'manually' visiting https://developer.accuwether.com, using the 
# location API

LOCID = '329821'

# APIKEY can be obtained by registering for a developer's trial account
# at https://developer.accuweather.com

APIKEY = 'Your_API_Key'

# Convert epoch time stamp to day of week
def dayOfWeek(ep):
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    index  = int(math.floor(ep / 86400 + 4) % 7)
    return weekdays[index]

# Dumps one forecast line to the printer
def forecast(idx):
	epoch = data['DailyForecasts'][idx]['EpochDate']
	day     = dayOfWeek(epoch)
 	lo      =  int(data['DailyForecasts'][idx]['Temperature']['Minimum']['Value'])
 	hi      =  int(data['DailyForecasts'][idx]['Temperature']['Maximum']['Value'])
 	amCond  =  data['DailyForecasts'][idx]['Day']['IconPhrase']
 	pmCond  =  data['DailyForecasts'][idx]['Night']['IconPhrase']
        printer.boldOn()
	printer.print(day)
        printer.print(':')
        printer.boldOff()
        printer.print(' low ')
        printer.print(lo)
	printer.print(deg)
	printer.print(' high ')
        printer.print( hi)
	printer.println(deg)
	printer.print('  AM: ')
        printer.println(amCond)
	printer.print('  PM: ')
        printer.println(pmCond)
        return

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch forecast data from Yahoo!, parse resulting XML
# grw - May 15, 2015
# Added try except logic to handle connection errors
# grw - Apr 19, 2016
# Updated Yahoo API query to new YQL format
# grw - Jan 5, 2018
# Switched to AccurWeather API and JSON

try:

  query_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + LOCID + '?apikey=' + APIKEY

#  print(query_url)

  response = ( urllib.urlopen(query_url).read())

  # print(response)
  # print('Loading json data from response string')
  data = json.loads(response)

  headline = data['Headline']['Text']

  # Print heading
  printer.boldOn()
  printer.print('{:^32}'.format('5 Day Forecast'))
  printer.boldOff()

  # Print head line
  printer.println('{:^32}'.format(headline))
  printer.println()

  forecast(0)
  forecast(1)
  forecast(2)
  forecast(3)
  forecast(4)
  printer.feed(3)

except:
  # printer.println('--Connection Error--')  # debugging 
  print (1) # send true value back to main
  exit(0)

print (0) # send false  value back to main

