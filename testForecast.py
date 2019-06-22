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
        print('Inside forecast')
        print('Index')
        print(idx)
        print('Getting epoch')
	epoch = data['DailyForecasts'][idx]['EpochDate']
        print(epoch)
        print('Getting day')
	day     = dayOfWeek(epoch)
        print(day)
        print('Getting lo temp')
 	lo      =  int(data['DailyForecasts'][idx]['Temperature']['Minimum']['Value'])
        print(lo)
        print('Getting hi temp')
 	hi      =  int(data['DailyForecasts'][idx]['Temperature']['Maximum']['Value'])
        print(hi)
        print('Getting daytime conditions')
 	amCond  =  data['DailyForecasts'][idx]['Day']['IconPhrase']
        print(amCond)
        print('Getting night conditions')
 	pmCond  =  data['DailyForecasts'][idx]['Night']['IconPhrase']
        print(pmCond)
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

  print(query_url)

#  response = ( urllib.urlopen(query_url).read())

  # Fake response to avoid using up our daily trial API limit
  response = '''
  {
  "Headline": {
    "EffectiveDate": "2019-01-04T07:00:00-05:00",
    "EffectiveEpochDate": 1546603200,
    "Severity": 3,
    "Text": "Expect rainy weather this morning through this evening",
    "Category": "rain",
    "EndDate": "2019-01-05T01:00:00-05:00",
    "EndEpochDate": 1546668000,
    "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/extended-weather-forecast/329821?lang=en-us",
    "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?lang=en-us"
  },
  "DailyForecasts": [
    {
      "Date": "2019-01-04T07:00:00-05:00",
      "EpochDate": 1546603200,
      "Temperature": {
        "Minimum": {
          "Value": 46,
          "Unit": "F",
          "UnitType": 18
        },
        "Maximum": {
          "Value": 55,
          "Unit": "F",
          "UnitType": 18
        }
      },
      "Day": {
        "Icon": 18,
        "IconPhrase": "Rain"
      },
      "Night": {
        "Icon": 12,
        "IconPhrase": "Showers"
      },
      "Sources": [
        "AccuWeather"
      ],
      "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=1&lang=en-us",
      "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=1&lang=en-us"
    },
    {
      "Date": "2019-01-05T07:00:00-05:00",
      "EpochDate": 1546689600,
      "Temperature": {
        "Minimum": {
          "Value": 39,
          "Unit": "F",
          "UnitType": 18
        },
        "Maximum": {
          "Value": 59,
          "Unit": "F",
          "UnitType": 18
        }
      },
      "Day": {
        "Icon": 2,
        "IconPhrase": "Mostly sunny"
      },
      "Night": {
        "Icon": 33,
        "IconPhrase": "Clear"
      },
      "Sources": [
        "AccuWeather"
      ],
      "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=2&lang=en-us",
      "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=2&lang=en-us"
    },
    {
      "Date": "2019-01-06T07:00:00-05:00",
      "EpochDate": 1546776000,
      "Temperature": {
        "Minimum": {
          "Value": 39,
          "Unit": "F",
          "UnitType": 18
        },
        "Maximum": {
          "Value": 64,
          "Unit": "F",
          "UnitType": 18
        }
      },
      "Day": {
        "Icon": 2,
        "IconPhrase": "Mostly sunny"
      },
      "Night": {
        "Icon": 35,
        "IconPhrase": "Partly cloudy"
      },
      "Sources": [
        "AccuWeather"
      ],
      "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=3&lang=en-us",
      "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=3&lang=en-us"
    },
    {
      "Date": "2019-01-07T07:00:00-05:00",
      "EpochDate": 1546862400,
      "Temperature": {
        "Minimum": {
          "Value": 48,
          "Unit": "F",
          "UnitType": 18
        },
        "Maximum": {
          "Value": 55,
          "Unit": "F",
          "UnitType": 18
        }
      },
      "Day": {
        "Icon": 3,
        "IconPhrase": "Partly sunny"
      },
      "Night": {
        "Icon": 36,
        "IconPhrase": "Intermittent clouds"
      },
      "Sources": [
        "AccuWeather"
      ],
      "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=4&lang=en-us",
      "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=4&lang=en-us"
    },
    {
      "Date": "2019-01-08T07:00:00-05:00",
      "EpochDate": 1546948800,
      "Temperature": {
        "Minimum": {
          "Value": 42,
          "Unit": "F",
          "UnitType": 18
        },
        "Maximum": {
          "Value": 66,
          "Unit": "F",
          "UnitType": 18
        }
      },
      "Day": {
        "Icon": 1,
        "IconPhrase": "Sunny"
      },
      "Night": {
        "Icon": 33,
        "IconPhrase": "Clear"
      },
      "Sources": [
        "AccuWeather"
      ],
      "MobileLink": "http://m.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=5&lang=en-us",
      "Link": "http://www.accuweather.com/en/us/durham-nc/27701/daily-weather-forecast/329821?day=5&lang=en-us"
    }
  ]
  }
  '''

  # print(response)
  # print('Loading json data from response string')
  data = json.loads(response)
  # print('Printing Type')
  # print(type(data))
  # print('Printing Headline:Text')
  # print(data['Headline']['Text'])
  conditions = data['Headline']['Text']

  # print('Printing DailyForecasts type')
  # print(type(data['DailyForecasts']))

  # print('Printing type list[0]')
  # print(type(data['DailyForecasts'][0]))
  # print('Printing list[0]:EpochDate')
  epoch =  data['DailyForecasts'][0]['EpochDate']

  # print(epoch)

  # print('converting to weekday')
  weekday = dayOfWeek(epoch)
  # print(weekday)

  # Print heading
  printer.boldOn()
  printer.print('{:^32}'.format('5 Day Forecast'))
  printer.boldOff()

  # Print current conditions
  printer.boldOn()
  printer.print('{:^32}'.format('Current conditions:')) 
  printer.boldOff()
  printer.println('{:^32}'.format(conditions))
  printer.println()
  print('Calling forecast 0')
  forecast(0)
  print('Calling forecast 1')
  forecast(1)
  print('Calling forecast 2')
  forecast(2)
  print('Calling forecast 3')
  forecast(3)
  print('Calling forecast 4')
  forecast(4)
  printer.feed(3)

except:
  # printer.println('--Connection Error--')  # debugging 
  print (1) # send true value back to main
  exit(0)

print (0) # send false  value back to main

