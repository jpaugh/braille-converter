# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''
functions used to perform the actual text substitution in order to
convert a text to Braille. These functions may operate on the Source
text, or upon rules from the lang files. In the later case, they are
forbidden from using rules whose type order is <= to the type order of
the rule they are translating. This prevents recursion problems, etc.
'''

import ds
from .util import fwarn

import re

#Identity - useful for unimplemented translations
ident = lambda r, c, w: w

#Used for trans functions that we anticipate implementing.
TODO = ident

def simple(rule, cxt, word):
  return word.replace(rule['prn'], rule['brl'])

def wcell(rule, cxt, word):
  '''
  Only translate if it matches the whole word.
  '''
  return ds.re.sub('\\b%s\\b' % rule['prn'], rule['brl'], word)

def capital(rule, cxt, word):
  '''
  Mark all capital letters as such.
  '''
  return ds.patt.capital.sub(rule['brl'] + '\\1', word).lower()

def letter(rule, cxt, word):
  '''
  Mark all words that are preceeded by a number.
  '''
  return ds.patt.letter.sub('\\1%s\\2' % rule['brl'], word).lower()

def number(rule, cxt, word):
  '''
  Mark all numbers as such.
  '''
  def repl(match):
    '''
    Prepend number mark and replace digits 1-9,0 with letters a-j
    '''
    word = match.group().split('')
    for i in xrange(word):
      l = word[i]
      if l == '0':
	word[i] = 'j'
      else:
	word[i] = chr(ord('a')-ord('1')+ ord(l))

    return rule['brl'] + ''.join(word)

  #TODO: translate 1-9,0 to A-J
  return ds.patt.number.sub(repl, word)

def decimal(rule, cxt, word):
  '''
  decimal point
  '''
  prn, brl = rule['prn'], rule['brl']
  i = 0
  while i > -1 and i < len(word)-1:
    i = word.find(prn, i)
    if i < 0 or i == len(word)-1:
      break
    elif ((word[i-1].isdigit() or not word[i-1].isalpha())
    and word[i+len(prn)].isdigit()):
      word = word[:i] + brl + word[i+len(prn)]
      i += len(brl)
    else:
      i += len(prn)

  return word

def bpunct(rule, cxt, word):
  '''
  opening punctuation (i.e. just quotation marks, for now)

  TODO: Catch "" and '' pairs
  '''
  bre = r'^([^\w]*)%s(\W*\w+)'
  bsub = r'\1%s\2'

  try:
    return re.sub(bre % rule['prn'], bsub % rule['brl'], word)
  except Exception as e:
    fwarn(cxt, e.message)
    return word

def epunct(rule, cxt, word):
  ere = r'(\w+\W*)%s(\W*)$'
  esub = r'\1%s\2'

  try:
    return re.sub(ere % rule['prn'], esub % rule['brl'], word)
  except Exception as e:
    fwarn(cxt, e.message)
    return word
