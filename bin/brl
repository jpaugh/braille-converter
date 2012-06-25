#!/usr/bin/env python
# start braile-converter
#
# Copyright 2012 Jonathan Paugh
# See COPYING for license details

import os, sys

if __name__ == '__main__':
  mypath = os.path.realpath(os.path.dirname(__file__))
  impath = os.path.dirname(mypath)

  init_file = os.path.join(impath, 'braille', '__init__.py')

  if os.path.isfile(init_file):
    sys.path.append(impath)

  from braille import __main__
