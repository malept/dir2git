#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

requires = []
extras = {
    'argcomplete': ['argcomplete'],
}

if sys.version_info < (2, 7):
    requires.append('argparse')

setup(name='dir2git',
      version='0.1',
      author='Mark Lee',
      scripts=['dir2git.py'],
      install_requires=requires,
      extras_require=extras)
