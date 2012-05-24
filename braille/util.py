#coding=utf8

import ds
from .options import opt


def warn(msg):
  '''
  Give a warning to the user on stderr, if we're in debug mode
  '''
  if opt('debug'):
    print >>opt('stderr'), msg
    opt('stderr').flush()


def fwarn(cxt, msg):
  '''
  Give a warning with file context information.
  '''
  warn('%s/%d: %s' % (cxt.fname, cxt.lineno, msg))


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

