#!/usr/bin/env python

from setuptools import setup, find_packages

import ssc

setup(
      name='SSC',

      version=ssc.__version__,

      description='Simple servlet container',

      author=ssc.__author__,

      author_email=ssc.__email__,

      package_dir={'ssc' : 'ssc'},

      packages=find_packages(),

	  license=ssc.__license__
)
