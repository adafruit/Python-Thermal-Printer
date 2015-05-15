from __future__ import print_function
__author__ = 'frza'

from adafruit import iotp_pool
from adafruit.tcp_interface import IotpTCPServer
from adafruit.amqp_interface import IotpAMQPServer
import time
import signal


class TestPrinter():
    def __init__(self):
        print("Test printer instantiated")

    def print(self, line):
        print(">> {}".format(line))

    def printImage(self, img):
        print(">> IMG")


def main(config):
    if config['printer_type'] == 'test':
        printer = TestPrinter()
    else:
        from adafruit.Adafruit_Thermal import Adafruit_Thermal
        printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    iotp_pool.init(printer)
    # start servers
    tcp_intf = IotpTCPServer(config)
    tcp_intf.start()

    amqp_intf = IotpAMQPServer(config)
    amqp_intf.start()

    while iotp_pool.is_running():
        time.sleep(1)

    tcp_intf.stop()
    amqp_intf.stop()


def activate_signal_handler(signal_handler_fun):
    '''
    Registers the given signal handler for a number of signals that may be sent to the process.
    signal_handler_fun: A function object with a signature like
    def f(signal_number, stack_frame): ...
    '''
    for s in [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGABRT, signal.SIGTERM]:
        signal.signal(s, signal_handler_fun)


if __name__ == '__main__':
    def exit_handler(signum, frame):
        iotp_pool.teardown()
        print("Exiting")

    activate_signal_handler(exit_handler)

    c = {'printer_type': 'test',
         # tcp props
         'TCP_HOST': '0.0.0.0',
         'TCP_PORT': 9999,
         # amqp props
         'AMQP_HOST': 'localhost'
        }
    main(c)
