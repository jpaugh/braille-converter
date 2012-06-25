# Copyright 2012 Jonathan Paugh
# See COPYING for license details
from . import *

#NOTE: Do this early
util.log.setupLogger()

import sys
from argparse import ArgumentParser

if version[0] == 0:
  #dev version: 0, major, minor, year, tag
  verfmt = '%d.%d.%d:%d-%s'
else:
  #release version: major, minor, year
  verfmt = '%d.%d.%d'

def argparseFactory(argspec):
  '''
  create an argparse.ArgumentParser from an input list. Does not support
  subparsers (yet).
  '''
  parser_spec = argspec[0]

  if not 'default' == parser_spec.get('type'):
    raise ValueError, 'default arg dict not found.'

  args, kwargs = parser_spec.get('args'), parser_spec.get('kwargs')
  parser = ArgumentParser(*args, **kwargs)

  group = parser_spec.get('group')
  if group:
    for argument in group:
      args, kwargs = argument.get('args'), argument.get('kwargs')
      parser.add_argument(*args, **kwargs)


  for i in xrange(1, len(argspec)):
    spec = argspec[i]
    typ = spec.get('type')
    group = spec.get('group')

    if not typ or not group:
      raise ValueError, 'Invalid type or group in argspec[%d]' % i

    if typ == 'exclusive':
      fun=ArgumentParser.add_mutually_exclusive_group
    elif typ == 'group':
      fun=ArgumentParser.add_argument_group
    else:
      raise ValueError, 'Unsupported group type: %s' % typ

    args, kwargs = spec.get('args'), spec.get('kwargs')
    group_parser = fun(parser, *args, **kwargs)

    for argument in group:
      args, kwargs = argument.get('args'), argument.get('kwargs')
      group_parser.add_argument(*args, **kwargs)
  return parser

argspec = [
    {
      'type': 'default',  # Default group (i.e. ungrouped arguments)
      'args': [],	  # Args for ArgumentParser()
      'kwargs': {
	'description': 'Convert text to Braille',
	},
      'group': [	  #List of arguments to add to parser
	{
	  'args': [ '--version' ],
	  'kwargs': {
	    'action': 'version',
	    'version': verfmt % version,
	    'help': 'display the current version of the software.',
	    },
	  },
	{
	  'args': [ '--log' ],
	  'kwargs': {
	    'nargs': 1,
	    'metavar':'LEVEL',
	    'dest': 'loglevel',
	    'help': 'change the log level. Values for LEVEL are CRITICAL, ERROR, WARNING, INFO, and DEBUG. The default is WARNING.',
	    },
	},
	{   #Args to parser.add_argument()
	  'args' : [ '-d', '--debug' ],
	  'kwargs': {
	    'action': 'store_const',
	    'dest': 'loglevel',
	    'const': ['DEBUG'],
	    'help': 'same as --log DEBUG',
	    },
	  },
	],
      },
    { # mutually exclusive group
      'type': 'exclusive',
      'args': [],	  #args to parser.add_mutually_exclusive()
      'kwargs': { 'required': False },
      'group': [	  #list of mu-exclusive args
	{
	  'args': [ '-gui', '--gui' ],	#args to group.add_argument()
	  'kwargs': {
	    'action': 'store_true',
	    'default': True,
	    'help': 'use the gui interface'
	    },
	  },
	{
	  'args': [ '-cmd', '--cmdline' ],
	  'kwargs': {
	    'action': 'store_false',
	    'dest': 'gui',
	    'help': 'use the command line interface',
	    },
	  },
	{
	  'args': ['--tests', ],
	  'kwargs': {
	    'action': 'store_true',
	    'help': 'run package tests, then exit; implies --log INFO'
	    },
	  },
	],
      },
    ]

cmdparser = argparseFactory(argspec)
args = cmdparser.parse_args()

if args.loglevel:
  args.loglevel = args.loglevel[-1].upper()
else:
  if args.tests:
    args.loglevel = 'INFO'
  else:
    args.loglevel='WARNING'
util.log.setLogLevel(args.loglevel)

if args.loglevel == 'DEBUG':
  opt('debug', True)

options.override(vars(args))

if opt('tests'):
  import unittest
  import unittest.runner

  tests = unittest.defaultTestLoader.discover('braille.tests', pattern='test*.py')
  runner = unittest.runner.TextTestRunner()
  runner.run(tests)

elif opt('gui'):
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
