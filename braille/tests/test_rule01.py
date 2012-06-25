# Copyright 2012 Jonathan Paugh
# See COPYING for license details
from . import EBAETestCase, dots

class RuleI(EBAETestCase):
  '''
  Punctuation Rules
  '''
  rule = 'I'

  def pairs(self):
    return (
	self.h('Punctuation Signs'),
	(',;:.!?/-', dots('2 23 25 256 235 236 34 36')),
	("a'a", dots('1 3 1')),
	('*', dots('35 35')),
	('...', dots('3 3 3')),
	('--', dots('36 36')),

	# Rule I.1 is 'Follow print practice' That's easy!

	self.sh ('Quotation Marks', go=2),
	('"a', dots('236 1')),
	('a"', dots('1 356')),
	("'a", dots('6 236 1')),
	("a'", dots('1 356 3')),
	('"I am coming."', dots('236 6 24  1 134  36 346 256 356')),
	('He said, "Sing \'Homing.\'"',
	  dots('6 125 15  234 145 2  236 6 234 346  6 236 6 125 135 134 346 256 356 3 356')),
	self.ss('Reverse quotation marks'),
	("He said, 'Sing \"Homing.\"'",
	  dots('6 125 15  234 145 2  6 236 6 234 346  236 6 125 135 134 346 256 356 356 3')),

	# Rule I.2.b we don't follow: reverse all quotes if print is reversed

	self.sh('Parentheses and Brakets'),
	('(', dots('2356')),
	(')', dots('2356')),
	('[', dots('6 2356')),
	(']', dots('2356 3')),
	('(said he)', dots('2356 234 145  125 15 2356')),
	('[see previous chapter]',
	  dots('6 2356 234 15 15  1234 1235 15 1236 24 1256 234  16 1 1234 2345 12456 2356 3')),
	('u(ni)form', dots('136 2356 1345 24 2356 123456 134')),
	('u[ni]ted', dots('136 6 2356 1345 24 2356 3 2345 1246')),
	('deci(sion)', dots('145 15 14 24 2356 46 1345 2356')),
	('cem(en)t', dots('14 15 134 2356 26 2356 2345')),

	self.sh('Apostrophes'),
	("'", dots('3')),
	#XXX("'tis", dots('3 2345 24 234')),
	("don't", dots('145 135 1345 3 2345')),
	#XXX Can't FIX: ("Jones'", dots('6 245 5 135 234 3')),

	#Rule 1.4.a has been omitted - "Insert omitted apostrophes"

	self.sh('Hyphen'),

	('self-control', dots('234 15 123 124 36 25 2345 1235 135 123')),
	('five- or six-pointed star',
	  dots('124 24 1236 15 36  135 1235  234 24 1346 36 1234 135 35 2345 1246  34 345')),

	#Rule 1.5.a has been omitted - Line breaking hyphenation
	# Instead, we'll follow print practice

	self.ss('hypens as omitted letters', go='b'),
	('l-m-n', dots('123 36 134 36 1345')),
	('Mr. J----', dots('6 134 1235 256  6 245 36 36 36 36')),

	#TODO: Rule I.6: Proper spacing of a dash (--)

	#TODO: Rule I.7: Space ellipsis as a word (and the rest)
      )
