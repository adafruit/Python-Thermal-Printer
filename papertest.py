#!/usr/bin/python

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

if printer.hasPaper():
	print("Has paper")
else:
	print("No paper")
