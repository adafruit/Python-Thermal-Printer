#!/usr/bin/python

import time

ledGreen    = 18
ledRed      = 24
buttonGreen = 23
buttonRed   = 25

def set(property, value):
	try:
		f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
		f.write(value)
		f.close()	
	except:
		print("Error writing to: " + property + " value: " + value)


set("mode", "pwm")
set("active", "1")

while(1):
	set("duty", "0")
	time.sleep(1)
	set("duty", "99")
	time.sleep(1)
