#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Use the Broadcom pin numbers (not Raspberry Pi pin numbers)
GPIO.setmode(GPIO.BCM)

ledGreen    = 18
ledRed      = 24
buttonGreen = 23
buttonRed   = 25

GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(ledRed  , GPIO.OUT)
GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonRed  , GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(1):
	GPIO.output(ledGreen, GPIO.HIGH)
	GPIO.output(ledRed  , GPIO.LOW)
	if(GPIO.input(buttonGreen) == False):
		print "Green button pressed"
		execfile('foo.py')
	if(GPIO.input(buttonRed) == False):
		print "Red button pressed"
#	time.sleep(1)
	GPIO.output(ledGreen, GPIO.LOW)
	GPIO.output(ledRed  , GPIO.HIGH)
	if(GPIO.input(buttonGreen) == False):
		print "Green button pressed"
		execfile('foo.py')
	if(GPIO.input(buttonRed) == False):
		print "Red button pressed"
#	time.sleep(1)

# Watch for 'falling' event on pin:
# (experimental stuff)
#GPIO.set_falling_event(pin)
#if(GPIO.event_detected(pin)):
#	print("Falling edge detected!")

# Reset all channels to inputs w/no pullup/dn
#GPIO.cleanup()
