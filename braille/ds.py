# Copyright 2012 Jonathan Paugh
# See COPYING for license details
from . import comp, trans
import re

class Context(object):
  '''
  Stores position info in a file or string source in an organised way.
  Generally useful for error messages (via fwarn).
  '''
  __slots__ = 'fname lineno pos'.split()


class T:
  '''
  Type enums - and some compound enums. These are used not only to check
  for programmer error: they are also used to check the lang files.
  '''
  abbrev = 'abbrev'
  accent = 'accent'
  bpunct = 'bpunct'
  capital = 'capital'
  char = 'char'
  cluster = 'cluster'
  decimal = 'decimal'
  epunct = 'epunct'
  italic = 'italic'
  letter = 'letter'
  mpunct = 'mpunct'
  nonlatin = 'nonlatin'
  number = 'number'
  prefix = 'prefix'
  punct = 'punct'
  wcell = 'wcell'
  space = 'space'
  unknown = None

  #list of types considered as "words"
  words = ( abbrev, char, cluster,
	    decimal, number, nonlatin,
	    prefix, wcell,
	  )

'''
Info about every rule of a (any) certain type.
   order: sort order
   comp: compilation function for the brl of a rule
   trans: translation function for source text that matches rules
'''
types = {
  T.bpunct  : {
    'order' :  0,
    'comp'  : comp.dotify,
    'trans' : trans.bpunct
    },
  T.epunct  : {
    'order' :  1,
    'comp'  : comp.dotify,
    'trans' : trans.epunct
    },
  T.mpunct  : {
    'order' :  2,
    'comp'  : comp.dotify,
    'trans' : trans.simple
    },
  T.decimal : {
    'order' :  3,
    'comp'  : comp.dotify,
    'trans' : trans.decimal
    },
  T.punct   : {
    'order' :  4,
    'comp'  : comp.dotify,
    'trans' : trans.simple
    },
  T.capital : {
    'order' :  5,
    'comp'  : comp.dotify,
    'trans' : trans.capital
    },
  T.abbrev  : {
    'order' :  6,
    'comp'  : comp.ident,
    'trans' : trans.simple
    },
  T.prefix  : {
    'order' :  7,
    'comp'  : comp.prefix,
    'trans' : trans.simple
    },
  T.wcell   : {
    'order' :  8,
    'comp'  : comp.ident,
    'trans' : trans.wcell
    },
  T.cluster : {
      'order' :  9,
      'comp' : comp.dotify,
      'trans' : trans.simple
      },
  T.number  : {
      'order' : 10,
      'comp' : comp.dotify,
      'trans' : trans.number
      },
  T.letter  : {
      'order' : 11,
      'comp' : comp.dotify,
      'trans' : trans.letter
      },
  T.nonlatin: {
      'order' : 12,
      'comp' : comp.dotify,
      'trans' : trans.ident
      },
  T.char    : {
      'order' : 13,
      'comp' : comp.dotify,
      'trans' : trans.simple
      },
  T.accent  : {
      'order' : -1,
      'comp' : comp.dotify,
      'trans' : trans.ident
      },
  T.italic  : {
      'order' : -1,
      'comp' : comp.dotify,
      'trans' : trans.ident
      },
  T.space   : {
      'order' : -1,
      'comp' : comp.ident,
      'trans' : trans.ident
      },
  T.unknown : {
      'order' : -1,
      'comp' : comp.ident,
      'trans' : trans.ident
      },
}

 
class patt:
  '''
  Regular expression patterns
  '''
  #Match a lang rule
  rule = re.compile(flags=re.X,
      pattern='''^\s*(?P<type>[^\\s]+)\\s+  #type
      ("|\')(?P<prn>[^\\2]*)\\2\\s+   #"print"	 (match string)
      ("|\')(?P<brl>[^\\4]*)\\4	      #"braille" (substitution string)
      (?:\\s+(?P<priority>\d+))?\\s*  # N (rule priority, optional)
      ''')

  #Match a valid dots pattern, with trailling garbage ignored
  dots = re.compile(flags=re.X, pattern='(\\d+\\s*)+')

  #Match the brl for a prefix, which is hybrid
  prefix = re.compile(flags=re.X,
      pattern='''(?P<dots>(\\d+\\s+)+)  #dots
      (?P<word>.*)''')			# word (ascii)

  #Match a token
  token = re.compile(flags=re.X,
      pattern='''([A-Za-z-]+  #Word
      |(?:[0-9]*\\.)[0-9]+    #Number
      |\\s+		      #Whitespace
      |.)''')		      #Any single char

  #Match /only/ whitespace
  space = re.compile(pattern='^\s+$')

  #Match capital letter(s)
  capital = re.compile('([A-Z])')
  #Match a capitalized word
  capword = re.compile('\\b[A-Z-][A-Z-]+\\b')

  #number
  number = re.compile('(?:[0-9]*\\.)[0-9]+')

  #letter preceeded by a number
  letter = re.compile('([0-9])([a-zA-Z])')
