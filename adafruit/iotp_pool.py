__author__ = 'frza'

from Queue import Queue
from threading import Thread
from adafruit.Adafruit_Thermal import Adafruit_Thermal
# from adafruit.iotp_pool_job import ImageJob

_q = Queue()


def enqueue(job):
    _q.put_nowait(job)


def teardown():
    enqueue('__quit__')


def size():
    return _q.qsize()


def _perform(printer, job):
    job.with_printer(printer)


def _worker(printer):
    print "Printer Job Queue started"
    while True:
        item = _q.get()
        if item == '__quit__':
            break
        else:
            _perform(printer, item)
    print "Exiting printer loop"


def init(**kwargs):
    printer = Adafruit_Thermal(**kwargs)
    t = Thread(target=_worker, args=printer)
    t.daemon = True
    t.start()
