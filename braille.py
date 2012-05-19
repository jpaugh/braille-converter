#!/usr/bin/env python
#to-braille - converts text to English Braile. encoding=utf8

import sys, re

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

def dots(s):
  '''
  convert a sequence of Braille dot patterns (string) to the
  corresponding Braille characters. NOTE: The dots for each cell must be
  separated by a single space. To include a literal space, use two dots
  instead.
  '''
  res = ''
  for word in s.split(' '):
    if word:
      res += dot(word)
    else:
      res += ' '

  return res

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

'''
Braille letters follow this pattern, which I want to take advantage of
to avoid data entry. :-) Every row (ten letters) of Braille repeats the
pattern, making a prescribed change to distinguish each set of 10.
Row 1 uses neither dot 3 or dot 6; Row 2 adds dot 3, Row 3 adds dot 6 to
the second row, and Row 3 omits dot 3. These three rows take us through
the alphabet--excepting w which was added to Braille as an afterthought.
'''
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

#Keep a tidy import
del b, i, c

#for letters u to z; this is sufficiently messed up that I do it by hand.
letters.extend((
  ('u', dot(patt[0]*100 + 36)),
  ('v', dot(patt[1]*100 + 36)),
  ('w', dot(patt[9]*100 + 6)),
  ('x', dot(patt[2]*100 + 36)),
  ('y', dot(patt[3]*100 + 36)),
  ('z', dot(patt[4]*100 + 36)),
  ))

'''
The letters and punctuation form the entirety of Uncontracted (Grade 1)
Braille, and what follows now is the definition of Grade 2 Braille.
'''

'''
The following data structures define the relationship between
Braille and English. The format of each is relatively similar, but
somewhat esortic in places. Specifically, The order in which these
structures are applied to the text /does/ matter, and they are defined
in the same order they should be processed in--including some individual
definitions. Also, some definitions make used of the latter fact, or of
some of the pecularities of Braille, which avoids converting to Braille
for as long as possible, but also makes some entries hard to decipher
for the non-Braillist.  Additionally, you must keep in mind that the
output of dot() is a string, and how the arithmetic operators work for
strings in Python.
'''

'''
Short forms - These are abbreviation for whole words, with the word on
the left and the contraction on the right. Keep in mind that some of
these will be contracted further by later processes--ex: con and ch are
contracted to one-cell forms.
'''
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

'''
Initial Letter contractions - Some words are abbreviated by prefixing
their initial letter with a certain cell. This is the most complicated
structure. We need to associate each prefix with the list of words that
can be contracted with it. Since the initial letter is used for the
contraction, we do not need to list the contracted form.  However, some
words require special care, because they are abreviated by a cell which
represents multiple English letters. These use a number in stead of
their initial letter, indicating how many letters to preserve.
Eventually, these letter groups will be contracted to their final form. 
'''

init_letter = (
    ( dot('5'), (
      'day',
      'ever',
      'father',
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
      '3there',
      '2character',
      '2through',
      '2where',
      'here',
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

'''
Final letter contractions - These are formed much as the initial letter
contractions, except that the prefix is followed by the final letter of
the expanded form, instead of the inital. Also, there are no final forms
using multiple letters, so no embedded counts are needed. 
'''

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

'''
One cell words - A select few words can be contracted to a single
cell, which disambiguation left up to the reader. Since this can be
quite confusing, one might assume that these contractions cannot be used
within a word, as are the part-word contractions, defined below.
However, I have not found a rule for this, and at least some of these
abbreviations (e.g. X=it) are acceptable either as a separate word, or
as a part-word contraction.
'''
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

'''
One cell part-words - These contractions may occur as part of a word, or
as a stand-alone word. Most of these stand for consonant or vowel
clusters, but a few stand for some words which commonly occur as part of
a word or alone. These must be encoded directly to Braille, as we are at
the last stage of contraction, followed by simple one-to-one substitutions
(i.e. Grade 1 Braille.)
'''

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

'''
Punctuation - This area of Braille presents the greatest opportunity for
error. In particular, we must attempt to determine the beginning and
ending of quotations, as well as whether each (') is a quote or an
apostrophe, while numerous semantic considerations are beyond the
purview of any machine algorithm, and can only be groped at
heuristically at best. This is not the only source of semantic woes, but
along with formatting guidelines, it represents one of the worst
contributers.
'''
#punctuation that occurrs only at the start of a word
st_punct = (
    ("'", brl.apostrophe + '"'),
    ('"', dot(236)),
    )

#punctuation that occurrs only at the end of a word
cl_punct = (
    ("'", '"' + brl.apostrophe),
    ('"', dot(356)),
    )

punctuation = (
    (',', dot(2)),
    (';', dot(23)),
    (':', dot(25)),
    ('...', brl.apostrophe * 3),
    ('.', dot(256)),
    ('!', dot(236)),
    ('[', dot(6) + ')'),
    (']', ')' + dot(3)),
    ('(', ')'),
    (')', dot(2356)),
    ('?', dot(236)),
    ('*', dot(35) *2),
    ('/', dot(34)),
    #All remaining 's assumed to be apostrophes
    ("'", brl.apostrophe),
    ('-', dot(36)),
    #XXX: Lacking: ditto sign
    )

def convert(line):
  '''
  converts a line of English (ASCII) text to Braille. For more
  information, consult the comments interspersed with the data
  structures, above.
  '''
  res = ''

  #Ignore silliness, vagueness, and wanton emptiness
  if not line:
    return line

  line = unicode(line).strip()
  
  for i in xrange(len(line)):
    c = ord(line[i])
    if c >= ord('A') and c <= ord('Z'):
      C = chr(c + 32)
      line = line[:i] + brl.capital + C + line[i+1:]

  for word in line.split():
    #Short forms
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

    for (p, b) in st_punct:
      word = re.sub(r'^([^\w]*)%s' % p, r'\1%s' % b, word)

    for (p, b) in cl_punct:
      word = re.sub(r'%s([^\w]*)$' % p, r'%s\1' % b, word)

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

    res += " " + word

  return res



if __name__ == '__main__':
  oline = ""
  while (True):
    line = sys.stdin.readline()

    oline = convert(line)

    #Helps readability on monospace outputs--like a terminal
    oline = oline.replace('', ' ')

    print oline.strip()
    oline = ''
