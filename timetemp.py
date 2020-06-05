#!/usr/bin/python

# Current time and temperature display for Raspberry Pi w/Adafruit Mini
# Thermal Printer.  Retrieves data from DarkSky.net's API, prints current
# conditions and time using large, friendly graphics.
# See forecast.py for a different weather example that's all text-based.
# Written by Adafruit Industries.  MIT license.
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import json
import time
import urllib
from PIL import Image, ImageDraw

from Adafruit_Thermal import *

API_KEY = "YOUR_API_KEY"

LAT = "40.726019"
LONG = "-74.00536"

# Fetch weather data from DarkSky, parse resulting JSON
url = "https://api.darksky.net/forecast/" + API_KEY + "/" + LAT + "," + LONG \
      + "?exclude=[alerts,minutely,hourly,flags]&units=us"
response = urllib.urlopen(url)
data = json.loads(response.read())

# Extract values relating to current temperature, humidity, wind

temperature = int(data['currently']['temperature'])
humidity = int(data['currently']['humidity'] * 100)
windSpeed = int(data['currently']['windSpeed'])
windDir = data['currently']['windBearing']
windUnits = "mph"

# print(temperature)
# print(humidity)
# print(windSpeed)
# print(windDir)
# print(windUnits)

# Although the Python Imaging Library does have nice font support,
# I opted here to use a raster bitmap for all of the glyphs instead.
# This allowed lots of control over kerning and such, and I didn't
# want to spend a lot of time hunting down a suitable font with a
# permissive license.
symbols = Image.open("gfx/timetemp.png")  # Bitmap w/all chars & symbols
img = Image.new("1", [330, 117], "white")  # Working 'background' image
draw = ImageDraw.Draw(img)

# These are the widths of certain glyphs within the 'symbols' bitmap
TimeDigitWidth = [38, 29, 38, 36, 40, 35, 37, 37, 38, 37, 13]
TempDigitWidth = [33, 25, 32, 31, 35, 30, 32, 32, 33, 32, 17, 14]
DateDigitWidth = [16, 13, 16, 15, 17, 15, 16, 16, 16, 16]
HumiDigitWidth = [14, 10, 14, 13, 15, 12, 13, 13, 13, 13, 18]
DayWidth = [104, 109, 62, 110, 88, 110, 95]
MonthWidth = [53, 52, 60, 67, 59, 63, 59, 56, 51, 48, 54, 53]
DirWidth = [23, 35, 12, 27, 15, 33, 19, 41, 23]
DirAngle = [23, 68, 113, 157, 203, 247, 293, 336]


# Generate a list of sub-image glyphs cropped from the symbols image
def croplist(widths, x, y, height):
    list = []
    for i in range(len(widths)):
        list.append(symbols.crop(
            [x, y + i * height, x + widths[i], y + (i + 1) * height]))
    return list


# Crop glyph lists (digits, days of week, etc.)
TimeDigit = croplist(TimeDigitWidth, 0, 0, 44)
TempDigit = croplist(TempDigitWidth, 40, 0, 39)
DateDigit = croplist(DateDigitWidth, 75, 0, 18)
HumiDigit = croplist(HumiDigitWidth, 75, 180, 16)
Day = croplist(DayWidth, 93, 0, 25)
Month = croplist(MonthWidth, 93, 175, 24)
Dir = croplist(DirWidth, 162, 175, 21)
# Crop a few odds-and-ends glyphs (not in lists)
Wind = symbols.crop([93, 463, 157, 479])
Humidity = symbols.crop([93, 479, 201, 500])
Kph = symbols.crop([156, 366, 196, 386])
Mph = symbols.crop([156, 387, 203, 407])

# Draw top & bottom bars
draw.rectangle([42, 0, 330, 3], fill="black")
draw.rectangle([42, 113, 330, 116], fill="black")

x = 42  # Initial drawing position
y = 12


# Paste a series of glyphs (mostly numbers) from string to img
def drawNums(str, x, y, list):
    for i in range(len(str)):
        d = ord(str[i]) - ord('0')
        img.paste(list[d], (x, y))
        x += list[d].size[0] + 1
    return x


# Determine total width of a series of glyphs in string
def numWidth(str, list):
    w = 0  # Cumulative width
    for i in range(len(str)):
        d = ord(str[i]) - ord('0')
        if i > 0: w += 1  # Space between digits
        w += list[d].size[0]  # Digit width
    return w


# Render current time (always 24 hour XX:XX format)
t = time.localtime()
drawNums(time.strftime("%H:%M", t), x, y, TimeDigit)

# Determine wider of day-of-week or date (for alignment)
s = str(t.tm_mday)  # Convert day of month to a string
w = MonthWidth[t.tm_mon - 1] + 6 + numWidth(s, DateDigit)
if DayWidth[t.tm_wday] > w: w = DayWidth[t.tm_wday]

# Draw day-of-week and date
x = img.size[0] - w  # Left alignment for two lines
img.paste(Day[t.tm_wday], (x, y))  # Draw day of week word
y += 27  # Next line
img.paste(Month[t.tm_mon - 1], (x, y))  # Draw month word
x += MonthWidth[t.tm_mon - 1] + 6  # Advance past month
drawNums(s, x, y, DateDigit)  # Draw day of month

x = 42  # Position for temperature
y = 67
# Degrees to string, remap '-' glyph, append degrees glyph
s = str(temperature).replace('-', ';') + ':'
drawNums(s, x, y, TempDigit)

# Determine wider of humidity or wind info
s = str(humidity) + ':'  # Appends percent glyph
s2 = str(windSpeed)
winDirNum = 0  # Wind direction glyph number
if windSpeed > 0:
    for winDirNum in range(len(DirAngle) - 1):
        if windDir < DirAngle[winDirNum]: break
winDirNum += 1
w = Humidity.size[0] + 5 + numWidth(s, HumiDigit)
w2 = Wind.size[0] + 5 + numWidth(s2, HumiDigit)
if windSpeed > 0:
    w2 += 3 + Dir[winDirNum].size[0]
if windUnits == 'kph':
    w2 += 3 + Kph.size[0]
else:
    w2 += 3 + Mph.size[0]
if w2 > w: w = w2

# Draw humidity and wind
x = img.size[0] - w  # Left-align the two lines
y = 67
img.paste(Humidity, (x, y))
x += Humidity.size[0] + 5
drawNums(s, x, y, HumiDigit)
x = img.size[0] - w  # Left-align again
y += 23  # And advance to next line
img.paste(Wind, (x, y))
x += Wind.size[0] + 5

if windSpeed > 0:
    img.paste(Dir[winDirNum], (x, y))
    x += Dir[winDirNum].size[0] + 3
x = drawNums(s2, x, y, HumiDigit) + 3
if windUnits == 'kph':
    img.paste(Kph, (x, y))
else:
    img.paste(Mph, (x, y))

# Open connection to printer and print image
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.printImage(img, True)
printer.feed(3)
