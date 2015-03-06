__author__ = 'frza'


class ImageJob(object):
    def __init__(self, image):
        self._image = image
        self._preprocess()

    @property
    def image(self):
        return self._image

    def _preprocess(self):
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

        # save
        self._image = img
