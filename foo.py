#!/usr/bin/python

# Must be run as root (due to GPIO access)

import RPi.GPIO as GPIO
import subprocess, time
from Adafruit_Thermal import *

ledPin    = 18
buttonPin = 23
holdTime  = 2
tapTime   = 0.01
printer   = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

def main():
  # Use Broadcom pin numbers (not Raspberry Pi pin numbers)
  GPIO.setmode(GPIO.BCM)

  # Enable LED and button (w/pull-up on latter)
  GPIO.setup(ledPin, GPIO.OUT)
  GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  # Print greeting image here

  poll()


def tap():
  print "Tap"
# subprocess.call(["python", "timetemp.py"])


def hold():
  print "Hold"
# Print 'goodbye' image and init shutdown
# subprocess.call("sync")
# subprocess.call(["shutdown", "-h", "now"])


# Need to make this poll twitter every 30 seconds
# And print sudoku and weather forecast once a day
def poll():

  # Poll initial button state and time
  prevButtonState = GPIO.input(buttonPin)
  prevTime        = time.clock()
  tapEnable       = False
  holdEnable      = False

  while(True):

    # Poll current button state and time
    buttonState = GPIO.input(buttonPin)
    t           = time.clock()

    # Has button state changed?
    if(buttonState != prevButtonState):
      prevButtonState = buttonState    # Yes, save new state/time
      prevTime        = t
    else:                              # Button state unchanged
      if((t - prevTime) >= holdTime):  # Button held more than 'holdTime'?
        # Yes it has.  Is the hold action as-yet untriggered?
        if(holdEnable == True):        # Yep!
          hold()                       # Perform hold action (usu. shutdown)
          holdEnable = False           # 1 shot...don't repeat hold action
          tapEnable  = False           # Don't do tap action on release
      elif((t - prevTime) >= tapTime): # Not holdTime.  tapTime elapsed?
        # Yes.  Debounced press or release...
        if(buttonState == True):       # Button released?
          if(tapEnable == True):       # Ignore if prior hold()
            tap()                      # Tap triggered (button released)
            tapEnable  = False         # Disable tap and hold
            holdEnable = False
        else:                          # Button pressed
          tapEnable  = True            # Enable tap and hold actions
          holdEnable = True


if __name__ == '__main__':
  main()
