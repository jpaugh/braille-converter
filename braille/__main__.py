from . import *

import sys
from argparse import ArgumentParser

if version[0] == 0:
  #dev version: 0, major, minor, year, tag
  verfmt = '%d.%d.%d:%d-%s'
else:
  #release version: year, major, minor
  verfmt = '%d.%d.%d'

cmdparser = ArgumentParser(description='Convert text to Braille')

cmdparser.add_argument('-d', '--debug', action='store_true',
    help='turn on warnings and debug messages')
#TODO: run tests from cmdline args
#cmdparser.add_argument('--tests', action='store_true',
#    help='run package tests, then exit')
cmdparser.add_argument('--version', action='version',
    version=verfmt % version,
    help='display the current version of the software.')

guiopt = cmdparser.add_mutually_exclusive_group()
guiopt.add_argument('-gui', '--gui', action='store_true',
    help='use the gui interface')
guiopt.add_argument('-cmd', '--cmdline', action='store_false',
    dest='gui', help='use the command line interface')

args = cmdparser.parse_args()

options.override(vars(args))

if opt('gui'):
  from . import gui
  gui.__main__()
else:
  oline = ""
  while (True):
    line = sys.stdin.readline()

    oline = convert(line)

    #Helps readability on monospace outputs--like a terminal
    oline = oline.replace('', ' ')

    print oline.strip()
    oline = ''
