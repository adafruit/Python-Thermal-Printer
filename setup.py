from distutils.core import setup #pylint: disable=import-error,no-name-in-module

PACKAGES = ['adafruit']
SCRIPTS = ['main.py']

setup(name='iotp_pool',
      version='0.0.1',
      description='adafruit iotp pool',
      author='Francesco Zanitti',
      author_email='fzanitti@gmail.com',
      packages=PACKAGES,
      scripts=SCRIPTS,
      install_requires=['pyserial',
                        'pillow',
                        'msgpack-python',
                        'pika',
                        ],
      )
