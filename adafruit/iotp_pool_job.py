from __future__ import print_function
__author__ = 'frza'
import uuid
import textwrap
import time


class BaseJob(object):
    def __init__(self):
        self._id = uuid.uuid4()
        self._state = 'created'
        self._ts = -1

    def queued(self):
        self._state = 'queued'

    @property
    def remove(self):
        return self.state == 'done' and int(time.time()) - self._ts > 30 * 60 * 1000

    @property
    def id(self):
        return self._id

    @property
    def id_str(self):
        return str(self._id)

    @property
    def state(self):
        return self._state

    def run(self, printer):
        self._state = 'running'
        self._with_printer(printer)
        self._state = 'done'
        self._ts = int(time.time())

    def _with_printer(self, printer):
        raise Exception('implement-me')


class SimpleTextJob(BaseJob):
    def __init__(self, text):
        super(SimpleTextJob, self).__init__()
        self._text = text

    def _with_printer(self, printer):
        wrapped = textwrap.wrap(self._text, width=32)
        for line in wrapped:
            printer.print(line + '\n')


class ImageJob(BaseJob):
    def __init__(self, image):
        super(ImageJob, self).__init__()
        self._image = image

    def _with_printer(self, printer):
        img = self._pre_process()
        printer.printImage(img)

    def _pre_process(self):
        img = self._image
        if img.mode != '1' or img.mode != 'L':
            img = img.convert(mode='1')

        # resize if w and h > 384
        w, h = img.size
        if w > 384 and h > 384:
            if w > h:
                h1 = 384
                w1 = w * h1 / h
            else:
                w1 = 384
                h1 = w1 * h / w
            img = img.resize(w1, h1)

        # rotate if w > 384
        w, _ = img.size
        if w > 384:
            img = img.rotate(90)

        return img


def create_job(obj):
    t = obj.get('type', None)
    if t is None:
        return None
    if t == 'simple_text':
        return SimpleTextJob(obj.get('text', ''))
    # elif t == 'image':
    return None
