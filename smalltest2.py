#!/usr/bin/python

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Print the 75x75 pixel logo in adalogo.py
import gfx.adaqrcode as adaqrcode
printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)
printer.feed(1)

