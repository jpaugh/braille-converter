# Copyright 2012 Jonathan Paugh
# See COPYING for license details
#coding=utf8

import ds
from .options import opt

import logging
import logging.config

def warn(*msg):
  '''
  Give a warning to the user on stderr, if we're in debug mode
  '''
  log.warn(*msg)
  log.debug('use of util.warn is deprecated')


def fwarn(cxt, msg):
  '''
  Give a warning with file context information.
  '''
  log.warn('%s/%d: %s' % (cxt.fname, cxt.lineno, msg))


def do_re(reg, s):
  '''
  Match a regex against a string, returning None or the matching dict.
  '''
  match = reg.match(s)
  if match:
    return match.groupdict()
  else:
    return None


def gettype(rule, key=None):
  '''
  Return something about a rule's type. If key is None (or absent,
  return the type itself.
  '''
  typ = rule['type']
  if not key:
    return ds.types[typ]
  else:
    return ds.types[typ][key]



def dots(s):
  '''
  convert a sequence of Braille dot patterns (string) to the
  corresponding Braille characters.

  NOTE: The dots for each cell must be separated by a single space. To
  include a literal space, use two dots instead.

  example: dots('123 135  1346  356') ==> u'\u2807\u2815 \u282d \u2834'
  == so it was
  '''
  res = ''
  for word in s.split(' '):
    if word:
      res += __dot(word)
    else: # empty string means add a space
      res += ' '

  return res


def __dot(s):
  '''
  helper for dots()

  Does not allow multiple dot patterns in one string, or non-digits.
  DOES work for 8bit dots (i.e. European Braille).

  example: __dot('234') ==> u'\280E' == ⠎
  '''
  if not s.isdigit():
    raise ValueError('Nondigits: "%s"' % s)

  num = 0x2800
  for n in (1,2,3,4,5,6,7,8):
    if str(n) in s:
      num |= 2**(n-1)

  return unichr(num)

class LogProxy(object):
  '''
  logs messages to the current logger
  '''
  default_logging_config = {
      'version':1,
      'formatters': {
	'simple': {
	  'format':
	  '[%(asctime)s] %(name)s:%(levelname)s:%(message)s',
	  },
	},
      'handlers': {
	'console': {
	  'class': 'logging.StreamHandler',
	  'level': 'DEBUG',
	  'formatter': 'simple',
	  'stream': 'ext://sys.stderr',
	  },
	},
      'loggers': {
	'braille': {
	  'level': 'WARNING',
	  'handlers': ['console',],
	  'propagate': 'yes',
	  },
	},
      }


  def changeLogger(self, name='braille'):
    if name in self.default_logging_config['loggers']:
      opt('logger', logging.getLogger(name))
    else:
      self.debug('unknown logger: %s', name)


  def setupLogger(self, lvl=None):
    logging.config.dictConfig(self.default_logging_config)
    self.changeLogger()
    if lvl:
      self.setLogLevel(lvl)
    return opt('logger')


  def setLogLevel(self, level):
    '''
    Only takes effect the first time it is called.
    '''
    if type(level) == str:
      nlvl = getattr(logging, level.upper(), None)

    if not type(nlvl) == int:
      warn('Invalid log level: %s' % level)
    else:
      opt('logger').setLevel(nlvl)


  def replaceHandlerStream(self, stream=None):
    '''
    Replace the stream that the underlying stream handler uses. This has
    no safety, so it is a bad idea! :-) But, on the other hand, even
    non-stream objects that support write() and flush() can be used.
    '''
    if not stream:
      stream = opt('stderr')

    logger = opt('logger')

    for handler in logger.handlers:
      if type(handler) == logging.StreamHandler:
	handler.stream = stream


  #Proxy methods
  def debug(self, *args, **kwargs):
    opt('logger').debug(*args, **kwargs)
    pass

  def info(self, *args, **kwargs):
    opt('logger').info(*args, **kwargs)
    pass

  def warn(self, *args, **kwargs):
    self.warning(*args, **kwargs)

  def warning(self, *args, **kwargs):
    opt('logger').warning(*args, **kwargs)
    pass

  def error(self, *args, **kwargs):
    opt('logger').error(*args, **kwargs)
    pass

  def exception(self, *args, **kwargs):
    opt('logger').exception(*args, **kwargs)
    pass

  def log(self, *args, **kwargs):
    opt('logger').log(*args, **kwargs)
    pass
log=LogProxy()

