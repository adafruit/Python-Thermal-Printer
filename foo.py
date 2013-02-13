#!/usr/bin/python

import RPi.GPIO as GPIO
import subprocess, time
from Adafruit_Thermal import *

def tapLeft():
	print "Tap left"
#	subprocess.call(["python", "smalltest.py"])
# Make this print the current time and date

def tapRight():
	print "Tap right"
#	subprocess.call(["python", "smalltest2.py"])
# ???
# Current weather?

def holdLeft():
	print "Hold left"
# ???

def holdRight():
	print "Hold right"
# ???

def holdBoth():
	print "Hold both"
	# Print 'goodbye' image and init shutdown


def poll():
	# Get initial button state and time
	pstate = 0
	if(GPIO.input(buttonGreen) == False): pstate += 1
	if(GPIO.input(buttonRed)   == False): pstate += 2
	ptime = time.clock()
	tflag = False
	hflag = False
	tstate = 0

	while(True):

		# Get new button state and current time
		state = 0
		if(GPIO.input(buttonGreen) == False): state += 1
		if(GPIO.input(buttonRed)   == False): state += 2
		t = time.clock()

		# Has button state changed?
		if(state != pstate):
			# Yes...save new state/time
			pstate = state
			ptime  = t
		else:
			# Button state is consistent.
			# Has it been held more than 'holdTime'?
			if((t - ptime) >= holdTime):
				# Yes.  Is the hold action as-yet untriggered?
				if(hflag == False):
					# Yes...
					if(state == 1):
						holdLeft()
					elif(state == 2):
						holdRight()
					elif(state == 3):
						holdBoth()
					hflag = True # Don't repeat hold action
					tflag = True # Don't do tap action on release
			# No, hasn't been holdTime yet.  Has tapTime elapsed?
			elif((t - ptime) >= tapTime):
				# Yes.  Button(s) released?
				if(state == 0):
					# Yes.  Debounced tap.
					if(tflag == False):
						if(hflag == False):
							# Release
							if(tstate == 1):
								tapLeft()
							elif(tstate == 2):
								tapRight()
							# There is no tap-both
						# Tap triggered; disable
						tflag = True
					hflag = False # Enable hold
				else:
					# Button pressed.  Enable tap action
					# and record button state.
					tflag  = False
					tstate = state




printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
printer.println("Hello!")


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

holdTime = 2
tapTime  = 0.01


poll()



#!/usr/bin/python

#import subprocess, time
#
#subprocess.call("sync")
#subprocess.call(["shutdown", "-h", "now"])

