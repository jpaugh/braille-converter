#!/usr/bin/python 
#to-braille - converts text to English Braile. encoding=utf8

import sys

def dot(s):
  '''
  convert a string of "dots" to a braille character.

  Does not expect multiple characters to be described by the dots. 
  DOES work for 8bit dots (i.e. European Braille).
  '''
  if type(s) == int:
    s = str(s)

  num = 0x2800
  for n in (1,2,3,4,5,6,7,8):
    if str(n) in s:
      num |= 2**(n-1)

  return unichr(num)

class brl:
  '''
  Assortment of string constants, each of which is a Braille cell.
  Unlike the other strings, these do not correspond to Latin letters, or
  the numerals.
  '''
  capital = dot(6)
  apostrophe = dot(3)
  number = dot(3456)
  letter = dot(56)

patt = (1, 12, 14, 145, 15, 124, 1245, 125, 24, 245)

letters = []

#for letters a to j
for i in range(10):
  b = dot(patt[i])
  c = chr(i+ord('a'))
  letters.append((c, b))

#for letters k to t
for i in range(10):
  b = dot(patt[i] * 10 + 3)
  c = chr(i+ord('k'))
  letters.append((c, b))

#for letters u to z; this is sufficiently messed up that I do it by hand.
letters.extend((
  ('u', dot(patt[0]*100 + 36)),
  ('v', dot(patt[1]*100 + 36)),
  ('w', dot(patt[9]*100 + 6)),
  ('x', dot(patt[2]*100 + 36)),
  ('y', dot(patt[3]*100 + 36)),
  ('z', dot(patt[4]*100 + 36)),
  ))

punctuation = (
    (',', dot(2)),
    (';', dot(23)),
    (':', dot(25)),
    ('.', dot(256)),
    ('!', dot(236)),
    ('[', dot(6) + ')'),
    (']', ')' + dot(6)),
    ('(', ')'),
    (')', dot(2356)),
    ('?', dot(236)),
    ('-', dot(36)),
    )

short_forms = (
    ('braille', 'brl'),
    ('children', 'chn'),
    ('conceive', 'concv'),
    ('could', 'cd'),
    ('deceive', 'dcv'),
    ('declare', 'dcl'),
    ('either', 'ei'),
    ('first', 'fst'),
    ('friend', 'fr'),
    ('good', 'gd'),
    ('great', 'grt'),
    ('herself', 'herf'),
    ('himself', 'hmf'),
    ('him', 'hm'),
    ('immediate', 'imm'),
    ('itself', 'itf'),
    ('letter', 'lr'),
    ('little', 'll'),
    ('much', 'mch'),
    ('must', 'mst'),
    ('myself', 'myf'),
    ('necessary', 'nec'),
    ("o'clock", 'o' + brl.apostrophe + 'c'),
    ('oneself', 'onef'),
    ('ourselves', 'ourvs'),
    ('paid', 'pd'),
    ('perceive', 'percv'),
    ('perhaps', 'perh'),
    ('quick', 'qk'),
    ('receive', 'rcv'),
    ('rejoice', 'rjc'),
    ('said', 'sd'),
    ('should', 'shd'),
    ('such', 'sch'),
    ('themselves', 'themvs'),
    ('thyself', 'thyf'),
    ('today', 'td'),
    ('to-day', 'td'),
    ('together', 'tgr'),
    ('tomorrow', 'tm'),
    ('to-morrow', 'tm'),
    ('tonight', 'tn'),
    ('to-night', 'tn'),
    ('would', 'wd'),
    ('yourselves', 'yrvs'),
    ('yourself', 'yrf'),
    ('your', 'yr'),
    )

init_letter = (
    ( dot('5'), (
      'day',
      'ever',
      'father',
      'here',
      'know',
      'lord',
      'mother',
      'name',
      'one',
      'part',
      'question',
      'right',
      'some',
      'time',
      'under',
      'work',
      'young',
      '3there',	  #'2...' means, use the first 2 chars of the word, rather than just the first, for the encoding.
      '2character',
      '2through',
      '2where',
      '2ought',
      )),
    ( dot('45'), (
      'upon',
      'word',
      '3these',
      '2those',
      '2whose',
      )),
    ( dot('456'), (
      'cannot',
      'had',
      'many',
      'spirit',
      'world',
      '3their',
      )),
    )

final_letter = (
    ( dot('46'), (
      'ound',
      'ance',
      'sion',
      'less',
      'ount',
      )),
    ( dot('56'), (
      'ence',
      'ong',
      'ful',
      'tion',
      'ness',
      'ment',
      'ity',
      )),
    ( dot('6'), (
      'ation',
      'ally',
      )),
    )

one_cell_words = (
    ('but', 'b'),
    ('can', 'c'),
    ('do', 'd'),
    ('every', 'e'),
    ('from', 'f'),
    ('go', 'g'),
    ('have', 'h'),
    ('just', 'j'),
    ('knowledge', 'k'),
    ('like', 'l'),
    ('more', 'm'),
    ('not', 'n'),
    ('people', 'p'),
    ('quite', 'q'),
    ('rather', 'r'),
    ('so', 's'),
    ('that', 't'),
    ('us', 'u'),
    ('very', 'v'),
    ('will', 'w'),
    ('it', 'x'),
    ('you', 'y'),
    ('as', 'z'),

    ('shall', 'sh'),
    ('this', 'th'),
    ('which', 'wh'),
    ('out', 'ou'),
    ('enough', 'en'),
    ('to', 'ff'),
    ('were', 'gg'),
    ('his', dot(' 23  6')),
    ('into', 'inff'),
    ('was', 'by'),
    ('still', 'st'),
    )

one_cell_parts = (
    ('and', dot('1234 6')),
    ('for', dot('123456')),
    ('of',  dot('123 56')),
    ('the', dot(' 234 6')),
    # with == wxh
    ('wxh',dot(' 23456')),
    ('ch',  dot('1    6')),
    ('gh',  dot('12   6')),
    ('sh',  dot('1  4 6')),
    ('th',  dot('1  456')),
    ('wh',  dot('1   56')),
    ('ed',  dot('12 4 6')),
    ('er',  dot('12 456')),
    ('ou',  dot('12  56')),
    ('ow',  dot(' 2 4 6')),
    ('ea',  dot(' 2')),
    ('be',  'bb'),
    ('bb',  dot(' 23')),
    ('con', 'cc'),
    ('cc',  dot(' 2  5')),
    ('dis', 'dd'),
    ('dd',  dot(' 2  56')),
    ('en',  dot(' 2   6')),
    ('ff',  dot(' 23 5')),
    ('gg',  dot(' 23 56')),
    ('ing', dot('  34 6')),
    ('in',  dot('  3 5')),
    ('by',  dot('  3 56')),
    ('st',  dot('  34')),
    ('ble', dot('  3456')),
    ('ar',  dot('  345')),
    ('com', dot('  3  6')),
    )

oline = ""
while (True):
  line = sys.stdin.readline()
  if not line:
    break
  line = unicode(line).strip()
  
  for i in xrange(len(line)):
    c = ord(line[i])
    if c >= ord('A') and c <= ord('Z'):
      C = chr(c + 32)
      line = line[:i] + brl.capital + C + line[i+1:]

  for word in line.split():
    #Short formhs
    for (lf, sf) in short_forms:
      word = word.replace(lf, sf)

    #two cell (initial letter contraction)
    for (prefix, conts) in init_letter:
      for c in conts:
	#sometimes, we need a 2- or 3-char prefix instead. (In Braille, it's still just one character.)
	if word[0].isdigit():
	  n=int(word[0])
	  word = word.replace(c, prefix + c[1:n+1])
	else:
	  word = word.replace(c, prefix + c[0])

    #two cell (final letter contraction)
    for (prefix, conts) in final_letter:
      for c in conts:
	word = word.replace(c, prefix + c[-1])

    #one cell stand-alone words
    #XXX: Doesn't exclude situations that allow compound words.
    #TODO: Find out if the above is actually necessary.
    for (oc, sf) in one_cell_words:
      word = word.replace(oc, sf)

    #one cell parts (can be stand-alone as well)
    for (oc, sf) in one_cell_parts:
      word = word.replace(oc, sf)

    #numbers
    in_num=False
    new_word=''
    for c in word:
      if c.isdigit():
	if not in_num:
	  new_word += brl.number
	in_num = True	# Begin digit sequence
	c = int(c)
	if c > 0:
	  new_word+= chr(c+ord('a')-1)
	else:
	  new_word+= chr(c+(ord('j')))
      else:
	if in_num and c.isalpha():  # letters after digit sequence
	  new_word+=brl.letter
	in_num = False	# End digit sequence
	new_word += c
    word = new_word

    #punctuation
    #TODO: Handle opening/closing quotes correctly
    for (p, b) in punctuation:
      word = word.replace(p,b)
	
    #letters
    for (c, b) in letters:
      word = word.replace(c, b)

    #Add a hair-space between cells; helps readablity
    #XXX This is only a problem for monospace fonts
    #word = word.replace('', unichr(0x200A))

    oline += " " + word

  print oline.strip()
  oline = ''
