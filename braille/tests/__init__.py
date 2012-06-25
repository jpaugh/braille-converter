# Copyright 2012 Jonathan Paugh
# See COPYING for license details
from braille import convert, dots, util
from braille.options import opt
import unittest

class BrTestCase(unittest.TestCase):
  '''
  Super-test class. All tests of the actual text translated should be
  based on this class. The subclasses call super(self.__class__,
  self).__init__(pairs), where pairs is an iterable of pairs in the
  form: (input, expected_output).

  In the midst of the pairs, any strings encountered will be printed.
  This allows headers to be printed for the tests, i.e.:

  pairs = [
    'First tests',
    ('test 1', '...'),
    ...

  There are three methods h, sh, and ss which generate headers,
  subheaders, and subsubheaders specifically for tests from the book.
  '''

  def setUp(self):
    self.pairs =  self.pairs()

  def pairs(self):
    '''
    return the list of pairs for the test
    '''
    return ()

  def test_rule(self):
    for pair in self.pairs:
      if type(pair) == str:
	util.log.info(pair)
      else:
	(prn, brl) = pair
	util.log.debug('  p <<%s>>' % prn)
	util.log.debug('  e << %s >>' % brl.replace('', ' '))
	util.log.debug('  g << %s >>' % convert(prn).replace('', ' '))
	self.assertEqual(brl, convert(prn))

class EBAETestCase(BrTestCase):
  '''
  Superclass for test cases that document our support for the rules from
  the English Braille: American Edition book. There are several methods
  defined here to generate headers for these tests, that show which rule
  of the book is being tested. These are h(), sh(), and ss(). These
  methods return strings which should be interspersed within the test
  pairs, like so:

  pairs = [
    self.h('Punctuation'),
    (',', dots('2')),
    ...
    self.sh(''),
    self.sh('Quotation Marks'),
    ('"', dots('236')),
    ...
    ...
  '''
  #Formatting strings
  header =    'Rule %s: %s'
  subheader = '     %s.%d: %s'
  ssheader =  '     %s.%d.%s: %s'

  #Formatting functions
  def h(self, msg):
    '''
    Print the header for this rule. (Should be called only once).
    '''
    if not getattr(self, 'rule', None):
      raise TypeError, 'self.rule must be specified'
    self._rule = self.rule
    return self.header % (self._rule, msg)

  def sh(self, msg, go=None):
    '''
    Return the next subheader. It automatically increments the subrule
    number each time it is called (and resets the subsubheader number).
    However, if you skip some subrules, set the go arument to the number
    of the next header to be printed.
    '''
    if go:
      self._sh = int(go)
    else:
      self._sh += 1
    self._ss = 0

    return self.subheader % (self._rule, self._sh, msg)

  def ss(self, msg, go=None):
    '''
    Return the next subsubheader. It automatically increments the
    subsubrule number each time it is called. However, you can manually
    set the number via the go argument, incase you skip some tests.
    '''
    if go:
      self._ss = str(go)
    else:
      if self._ss:
	self._ss = chr(ord(_ss) + 1)
      else:
	self._ss = 'a'

    return self.ssheader % (self._rule, self._sh, self._ss, msg)

