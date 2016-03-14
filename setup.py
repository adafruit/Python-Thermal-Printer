'''
Adadfruit_Thermal - a python library for interacting with TTL serial
thermal printers from Adafruit.

Copyright 2013 2014, 2015, 2016 Adafruit Industries
See AUTHORS file for full list of contributors

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='Adafruit_Thermal',
      version='1.0.0',
      description='Library for controlling Adafruit Thermal Printers',
      url='https://github.com/bareo/Python-Thermal-Printer',
      author='zach wick',
      author_email='zwick@bareo.io',
      license='MIT',
      packages=['Adafruit_Thermal'],
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 2.7',
      ],
      install_requires=[
          'pyserial',
          'Pillow',
          'unidecode',
      ],
      keywords='adafruit thermal printer serial',
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
  )
