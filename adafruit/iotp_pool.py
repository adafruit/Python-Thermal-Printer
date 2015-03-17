__author__ = 'frza'

from Queue import Queue
from threading import Thread

_q = Queue()

all_jobs = {}


def job_state(job_id):
    if job_id in all_jobs:
        return all_jobs[job_id].state
    return False


def is_running():
    return _q is not None


def enqueue(job):
    all_jobs[job.id_str] = job
    job.queued()
    if len(all_jobs) > 1000:
        rm = []
        for k, v in all_jobs:
            if v.remove():
                rm.append(k)
        for jid in rm:
            print "Removing old job {}".format(jid)
            del(all_jobs[jid])
    _q.put_nowait(job)


def teardown():
    enqueue('__quit__')


def size():
    return _q.qsize()


def _perform(printer, job):
    print "Start job {}".format(str(job.id))
    job.run(printer)
    print "Done job {}".format(str(job.id))


def _worker(printer):
    global _q
    print "Printer Job Queue started"
    while True:
        item = _q.get()
        if item == '__quit__':
            break
        else:
            _perform(printer, item)
    print "Exiting printer loop"
    _q = None


def init(printer):
    t = Thread(target=_worker, args=[printer])
    t.daemon = True
    t.start()
