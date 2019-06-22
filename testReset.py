#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *

ledPin       = 18

printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)


GPIO.output(ledPin, GPIO.HIGH)

printer.println('Testing Network')

errortime = time.asctime( time.localtime(time.time()) )
printer.println(errortime)

printer.println('Stoping wlan0')
subprocess.call(["sudo", "stopWifi.sh"])
time.sleep(10)

printer.println('Checking Network')

try:
  subprocess.check_call(["sudo", "checkWifi.sh"])
  printer.println('Network OK')
  
except:
  # Show network error information

  printer.boldOn()
  printer.println('Network is unreachable')
  printer.underlineOn()
  printer.println('Resetting Connection')
  printer.underlineOff()
  printer.boldOff()

  # Reset wifi
  subprocess.call(["sudo", "resetWifi.sh"])
  time.sleep(30)

  # Test Network and show result
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    printer.feed(1)
    printer.print('My IP address is ' + s.getsockname()[0])
  except:
    printer.println('Network is still unreachable.')

printer.feed(3)

GPIO.output(ledPin, GPIO.LOW)

