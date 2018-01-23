Python-Thermal-Printer
======================

Installation::

    pip install Adafruit_Thermal

or::

    python setup.py install

Usage::

    >>> import Adafruit_Thermal
    >>> printer = Adafruit_Thermal('/dev/ttyAMA0', 19200, timeout=5)
    >>> printer.println('Hello World!')

