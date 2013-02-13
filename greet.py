#!/usr/bin/python

from __future__ import print_function
from Adafruit_Thermal import *
import Image

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Because the hello/goodbye images are overall fairly light, we can
# get away with using a darker heat time for these, then reset to the
# default afterward.
ht = int(printer.defaultHeatTime * 1.5)
if(ht > 255): ht = 255

#printer.begin(ht) # Set temporary dark heat time
img      = Image.open('gfx/hello.png')
printer.printImage(img, True)
printer.feed(3)
#printer.begin() # Reset default heat time

#printer.begin(ht) # Set temporary dark heat time
img      = Image.open('gfx/goodbye.png')
printer.printImage(img, True)
printer.feed(3)
#printer.begin() # Reset default heat time

