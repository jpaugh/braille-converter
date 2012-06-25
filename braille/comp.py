# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''
functions used to compile brl expressions into their final form. This is
needed because the lang files don't use Braille at all! They use latin
letters along with dot patterns.
'''

from .util import fwarn, dots

#Compilation identity
ident = lambda c, r: r

#Comp functions are *destructive*! Rule is modified in-place.
def dotify(cxt, rule):
  '''
  Attempt to interpret the brl of the rule as a dot pattern.
  '''
  try:
    rule['brl'] = dots(rule['brl'])
  except ValueError as e:
    fwarn(cxt, 'Bad dot pattern in rule %s\n%s' % (rule, e.message))

def try_dotify(cxt, rule):
  '''
  Attempt to interpret the rule's brl as a dot pattern. failure is
  silent, since most rules will fail.
  '''
  # We split so that each word can be tried separately.
  words = rule['brl'].split(' ')
  for i in xrange(len(words)):
    try:
      words[i] = dots(words[i])
    except ValueError:
      pass
  rule['brl'] = ' '.join(words)

def prefix(cxt, rule):
  try_dotify(cxt, rule)
  rule['brl'] = rule['brl'].replace(' ', '')

