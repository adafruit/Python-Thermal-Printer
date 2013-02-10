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

holdtime = 3
taptime  = 0.01

# Need to distinguish between 'taps' and 'holds' -- but also debounces.
# Left/right tap, left/right hold, both hold.
# Any button press/release resets timer.

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
		# Has it been held more than 'holdtime'?
		if((t - ptime) >= holdtime):
			# Yes.  Is the hold action as-yet untriggered?
			if(hflag == False):
				# Yes...
				if(state == 1):
					# Hold left
					print "Hold left"
				elif(state == 2):
					# Hold right
					print "Hold right"
				elif(state == 3):
					# Hold both
					print "Hold both"
				hflag = True # Don't repeat hold action
				tflag = True # Don't do tap action on release
		# No, hasn't been holdtime yet.  Has taptime elapsed?
		elif((t - ptime) >= taptime):
			# Yes.  Button(s) released?
			if(state == 0):
				# Yes.  Debounced tap.
				if(tflag == False):
					if(hflag == False):
						# Release
						if(tstate == 1):
							# Tap left
							print "Tap left"
						elif(tstate == 2):
							# Tap right
							print "Tap right"
						# There is no tap-both
					# Tap triggered; disable
					tflag = True
				hflag = False # Enable hold
			else:
				# Button pressed.  Enable tap action
				# and record button state.
				tflag  = False
				tstate = state


