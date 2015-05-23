#!/usr/bin/env python

from distutils.core import setup

import ssc

setup(
      name = 'SSC',
      
      version = ssc.__version__,
      
      description = 'Simple servlet container',
      
      author = ssc.__author__,
      
      author_email = ssc.__email__,
      
      package_dir = {'ssc' : 'ssc'},
      
      packages = ['ssc', 'ssc' ],
	  
	  license = ssc.__license__
)
