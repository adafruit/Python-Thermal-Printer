__author__ = 'frza'

from adafruit import iotp_pool
from adafruit.tcp_interface import IotpTCPServer
import time


def main(**kwargs):
    iotp_pool.init(**kwargs)
    # start servers
    tcp_intf = IotpTCPServer(**kwargs)
    tcp_intf.start()

    # TODO: intercept signal to exit gracefully
    while True:
        time.sleep(30)


if __name__ == '__main__':
    main()