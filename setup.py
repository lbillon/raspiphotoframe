#!/usr/bin/env python

from distutils.core import setup

setup(name='raspiphotoframe',
      version='1.0',
      py_modules=['raspiphotoframe'],
      scripts=['bin/raspiphotoframe-run', 'bin/raspiphotoframe-scan',
               'bin/raspi-screen'], )
