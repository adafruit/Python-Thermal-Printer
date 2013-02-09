#!/usr/bin/python

from __future__ import print_function
from Adafruit_Thermal import *
import Image

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

img      = Image.open('gfx/hello.png')
printer.printImage(img)
printer.feed(3)

img      = Image.open('gfx/goodbye.png')
printer.printImage(img)
printer.feed(3)

