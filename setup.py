#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'artnet/_version.py'
versioneer.versionfile_build = None
versioneer.tag_prefix = 'v'
versioneer.parentdir_prefix = 'py-artnet-'

setup(name="py-artnet",
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Python bindings for libartnet',
      author='Fredrik Lindberg',
      author_email='fli@shapeshifter.se',
      packages=['artnet', 'artnet/port'],
    )
