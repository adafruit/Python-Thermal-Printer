#!/usr/bin/python

from __future__ import print_function
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
printer.begin(0)

# Progressively increase heat time settings.
# Paper will jam or unit will reset at some point.
# Use last printed number as heat setting in future.
for i in range(0,256,15):
	printer.begin(i)
	printer.println(i)
	printer.inverseOn()
	printer.print('{:^32}'.format(''))
	printer.inverseOff()
printer.feed(4)

