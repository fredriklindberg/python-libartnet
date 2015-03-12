#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="py-artnet",
      version=0,
      description='Python bindings for libartnet',
      author='Fredrik Lindberg',
      author_email='fli@shapeshifter.se',
      packages=['artnet', 'artnet/port'],
    )
