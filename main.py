#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *

ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
amFlag       = False # Set after morning daily trigger occurs
pmFlag       = False # Set after afternoon trigger occurs
lastId       = '1'   # State information passed to/from interval script

nextCadence  = 0.0   # Time of next recurring operation
lastUpdate   = '2015-05-26T19:34:59+00:00' # Time of last weather alert update

nextCheck    = 0.0

printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

needForecast = 0           # New variable to run forcast
unknownIP    = '?.?.?.?'   # String to indicate no IP address available
ipAddress    = unknownIP   # IP Address to print

solvedFlag   = False       # True after sudoku solution printed 


# Called when button is briefly tapped.  Invokes time/temperature script.
def tap():
  global solvedFlag
  result = checkNetwork(True)
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  printer.feed(1)


  if result:
    subprocess.call(["python", "timetemp.py"])

  # show solution on first tap
  if solvedFlag == False:
    subprocess.call(["python", "sudoku-gfx.py", "puzzle.txt"])
    solvedFlag = True

  GPIO.output(ledPin, GPIO.LOW)


# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  printer.printImage(Image.open('gfx/goodbye.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin, GPIO.LOW)


# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def interval():
  GPIO.output(ledPin, GPIO.HIGH)
  p = subprocess.Popen(["python", "twitter.py", str(lastId)],
    stdout=subprocess.PIPE)
  GPIO.output(ledPin, GPIO.LOW)
  return p.communicate()[0] # Script pipes back lastId, returned to main

# Called at regular intervals (15 minutess by default).
# Invokes alerts script.
def cadence():
  GPIO.output(ledPin, GPIO.HIGH)
  p = subprocess.Popen(["python", "alerts.py", str(lastUpdate)],
    stdout=subprocess.PIPE)
  GPIO.output(ledPin, GPIO.LOW)
  return p.communicate()[0] # Script pipes back lastUpdate, returned to main

def weather():
  GPIO.output(ledPin, GPIO.HIGH)
#  printer.println('Calling Forecast.py')
  p = subprocess.Popen(["python", "forecast.py"],
    stdout=subprocess.PIPE)
  GPIO.output(ledPin, GPIO.LOW)
  return p.communicate()[0] # Script pipes back result, returned to main
  

# Called once per day (6:30am by default).
# Invokes weather forecast and sudoku-gfx scripts.

def daily():
  global solvedFlag
  GPIO.output(ledPin, GPIO.HIGH)
  # subprocess.call(["python", "forecast.py"])

  subprocess.call(["python", "sudoku-gfx.py"])
  solvedFlag = False  #a new puzzle is unsolved
  GPIO.output(ledPin, GPIO.LOW)

# Check the network status and result
# Verbose mode will print messages
# Returns True if network is okay
def checkNetwork(verbose):
  GPIO.output(ledPin, GPIO.HIGH)
  try:
    subprocess.check_call(["sudo", "checkWifi.sh"])
    if verbose:
      printIP()
    return True
  except:
    # Show network error information
    errortime = time.asctime( time.localtime(time.time()) )
    
    if verbose:
      printer.boldOn()
      printer.println(errortime)
      printer.println('Network is unreachable')
      printer.underlineOn()
      printer.println('Resetting Connection')
      printer.underlineOff()
      printer.boldOff()
    
    # Reset wifi
    subprocess.call(["sudo", "resetWifi.sh"])
    # wait for wifi to reset
    time.sleep(30)

    # Test Network and show result
    try:
        setIP()
        if verbose:
          printIP()
          # print msg if down, and reset OK
          printer.println(errortime + ': Up')
    except:
        if verbose:
          printer.println('Network is still unreachable.')
          printer.feed(1)
        else:
          # print terse msg if down, and can't reset
          printer.println(errortime + ': Down')
        return False

    if verbose:
      printer.feed(1)
    return True

  GPIO.output(ledPin, GPIO.LOW)

# Set the IP address
# throws connection error if cannot reach the network
def setIP():
  global ipAddress

  ipAddress = unknownIP

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 0))
  ipAddress = s.getsockname()[0]

# Print the IP Address
def printIP():
  printer.feed(1)
  printer.println('My IP address is ' + ipAddress)


# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(30)

# Show IP address (if network is available)
try:
  setIP()        
  printIP()
except:
  printer.feed(1)
  printer.boldOn()
  printer.println('Network is unreachable.')
  printer.boldOff()
  printer.print('Connect display and keyboard\n'
    'for network troubleshooting.')
  printer.feed(3)
  exit(0)

# Print greeting image
printer.printImage(Image.open('gfx/hello.png'), True)
printer.feed(3)
GPIO.output(ledPin, GPIO.LOW)

# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

# Main loop
while(True):

  # Poll current button state and time
  buttonState = GPIO.input(buttonPin)
  t           = time.time()

  # Has button state changed?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # Yes, save new state/time
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
      # Yes it has.  Is the hold action as-yet untriggered?
      if holdEnable == True:        # Yep!
        hold()                      # Perform hold action (usu. shutdown)
        holdEnable = False          # 1 shot...don't repeat hold action
        tapEnable  = False          # Don't do tap action on release
    elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
      # Yes.  Debounced press or release...
      if buttonState == True:       # Button released?
        if tapEnable == True:       # Ignore if prior hold()
          tap()                     # Tap triggered (button released)
          tapEnable  = False        # Disable tap and hold
          holdEnable = False
      else:                         # Button pressed
        tapEnable  = True           # Enable tap and hold actions
        holdEnable = True

  # LED blinks while idle, for a brief interval every 2 seconds.
  # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
  # the PWM-related library is a hassle for average users to install
  # right now.  Might return to this later when it's more accessible.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)

  # Once per day (currently set for 6:30am local time, or when script
  # is first run, if after 6:30am), run forecast and sudoku scripts.
  l = time.localtime()
  if (60 * l.tm_hour + l.tm_min) > (60 * 6 + 30):
    if amFlag == False:
      daily()
      amFlag = True
      needForecast = 1
  else:
    amFlag = False  # Reset daily trigger

  # Every afternoon, at 4:30pm get the evening forecast
  if (60 * l.tm_hour + l.tm_min) > (60 * 16 + 30):
    if pmFlag == False:
      pmFlag = True
      needForecast = 1
      # subprocess.call(["python", "sudoku-gfx.py", "puzzle.txt"])
      GPIO.output(ledPin, GPIO.LOW)
  else:
    pmFlag = False  # Reset daily trigger


  # Every 30 seconds, run Twitter scripts.  'lastId' is passed around
  # to preserve state between invocations.  Probably simpler to do an
  # import thing.
  if t > nextInterval:
    nextInterval = t + 30.0

    # printer.println('needForecast = ', needForecast)

    if needForecast:
      # printer.println('calling weather')
      result = weather()

      if result is not None: 
        try:
          needForecast = int(result.rstrip('\r\n'))
        except:
          # keep trying until yahoo responds with valid forecast
          needForecast = 1
      else:
        # keep trying until yahoo responds to request
	needForecast = 1

      # debugging print value returned and needForecast
      # printer.feed(1)
      # printer.print('result = ', result)  
      # printer.print('needForecast = ', needForecast)
      # printer.feed(2)

    result = interval()

    if result is not None:
      lastId = result.rstrip('\r\n')

    # debugging print value returned and lastid
    # printer.feed(1)
    # printer.print ('result = ', result)  
    # printer.print ('lastId = ', lastId)
    # printer.feed(2)

  # Every 10 minutes check weather alerts 
  if t > nextCadence:
    nextCadence = t + 600.0

    result = cadence()

    if result is not None:
      lastUpdate = result.rstrip('\r\n')

    # debugging print value returned and lastid
    # printer.feed(1)
    # printer.print ('result = ', result)  
    # printer.print ('lastId = ', lastId)
    # printer.feed(2)

  # Every 30 minutes check wifi 
  if t > nextCheck:
    nextCheck = t + 1800.0

    checkNetwork(False)






    

 
