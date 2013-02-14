#!/usr/bin/python

# This is a Python port of Adafruit's "Gutenbird" sketch for Arduino.
# Polls one or more Twitter accounts for changes, displaying updates
# on attached thermal printer.
# Written by Adafruit Industries.  MIT license.
# 
# Required hardware includes an Internet-connected system with Python
# (such as Raspberry Pi) and an Adafruit Mini Thermal Receipt printer
# and all related power supplies and cabling.
# Required software includes Adafruit_Thermal and PySerial libraries.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import sys, urllib, json, time, HTMLParser
from unidecode import unidecode
from Adafruit_Thermal import *

# queryString can be any valid Twitter API search string, including
# boolean operators.  See https://dev.twitter.com/docs/using-search
# for options and syntax.  Funny characters do NOT need to be URL
# encoded here -- urllib takes care of that.
queryString = 'from:Adafruit'

# These shouldn't need to be changed:
serverName  = 'search.twitter.com'
printer     = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
# lastID is command line value (if passed), else 1
if len(sys.argv) > 1: lastId = sys.argv[1]
else:                 lastId = '1'

url    = ('http://search.twitter.com/search.json?' +
          urllib.urlencode(dict(q=queryString)) +
          '&rpp=5&since_id=' + lastId)
data   = json.load(urllib.urlopen(url))
lastId = data['max_id_str']

for tweet in data['results']:

  printer.inverseOn()
  printer.print(' ' + '{:<31}'.format(tweet['from_user']))
  printer.inverseOff()

  printer.underlineOn()
  printer.print('{:<32}'.format(tweet['created_at']))
  printer.underlineOff()

  # Remove HTML escape sequences
  # and remap Unicode values to nearest ASCII equivalents
  printer.print(unidecode(
    HTMLParser.HTMLParser().unescape(tweet['text'])))

  printer.feed(3)

print(lastId) # Piped back to calling process
