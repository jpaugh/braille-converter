# Copyright 2012 Jonathan Paugh
# See COPYING for license details
from . import BrTestCase, dots

class Regressions(BrTestCase):
  def pairs(self):
    return (
	'refined match for wcells: 145b9f642ec083bdf25b25268dfa1bc33a4dadc2',
	('was.', dots('356 256')),
	('but-this', dots('12 36 1456')),
	'Abbrevs should be translated before prefixes 0f427bb2294e6f773e872d67d95b2c41153dfbe4',
	('today', dots('2345 145')),
	)

