#!/usr/bin/env python
#to-braille - converts text to English Braile. encoding=utf8

import sys, re

version = (0, 1, 0, 2002, 'beta')

class T:
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
  unknown = None

  '''
  list of types considered as "words"
  '''
  words = ( abbrev, char, cluster,
	    decimal, number, nonlatin,
	    prefix, wcell,
	  )

def warn(msg):
  '''
  Give a warning to the user on stderr
  '''
  print >>sys.stderr, msg
  sys.stderr.flush()

def fwarn(cxt, msg):
  '''
  Give a warning with file context information
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


def import_language(lang):
  '''
  loads the rules for the given language
  '''
  import os
  lang = lang.replace('_', '-')

  #Import standard (international) rules first
  if not lang == 'standard':
    rules = import_language('standard')
  else:
    rules = []

  class Context: pass
  cxt = Context()
  cxt.fname = os.path.join('lang', lang)
  cxt.lineno = 0

  try:
    with open(cxt.fname) as lfile:
      for rule in lfile:
	cxt.lineno += 1
	r = parse_rule(cxt, rule)
	if r:
	  rules.append(r)
  except IOError as e:
    raise

  rules.sort(cmp=cmp_rules)
  return rules


def parse_rule(cxt, rule):
  '''
  parse a string into a rule tuple
  '''
  rule = rule.strip()
  if (not rule) or rule[0] == '#':
    return None
  match = do_re(patt.rule, rule)
  if not match:
    fwarn(cxt, 'Invalid Rule "%s"' % rule)
    return None
  typ = match['type'].lower()

  if not typ in types:
    fwarn(cxt, 'Unknown rule type: '+typ)
    return None

  match['type'] = typ
  if not match['priority']:
    match['priority'] = 1
  return match


def cmp_rules(x, y):
  '''
  cmp function for the rules.
  '''
  if types[x['type']] < types[y['type']]:
    return -1
  elif types[x['type']] > types[y['type']]:
    return 1
  elif x['priority'] < y['priority']:
    return -1
  elif x['priority'] > y['priority']:
    return 1
  else:
    # Longer strings first
    return -1 * cmp(len(x['prn']), len(y['prn']))

class patt:
  #Match a lang rule
  rule = re.compile(flags=re.X,
      pattern='''(?P<type>[^\s]+)\s+  #type
      ("|\')(?P<prn>[^\\2]*)\\2\s+    #"print"	 (match string)
      ("|\')(?P<brl>[^\\4]*)\\4	      #"braille" (substitution string)
      (?:\s+(?P<priority>\d+))?''')   # 1 (rule priority)

  #Match a valid dots pattern, with trailling garbage ignored
  dots = re.compile(flags=re.X, pattern='(\\d+\\s*)+')

  #Match the brl for a prefix, which is hybrid
  prefix = re.compile(flags=re.X,
      pattern='''(?P<dots>(\\d+\\s+)+)  #dots
      (?P<word>.*)''')		      # word (ascii)

  #Match the first token
  token = re.compile(flags=re.X,
      pattern='''([A-Za-z-]+  #Word
      |(?:[0-9]*\\.)[0-9]+  #Number
      |\\s+		    #Whitespace
      |.)''')		    #Any single char

  #Match /only/ whitespace
  space = re.compile(pattern='^\s+$')


#Type info
#   order: sort order
#   reduce: fun to reduce the brl of any rule of this type
#   parse:  parsing strategy (function) for when this rule matches
types = {
  T.bpunct  : { 'order' :  0, 'parse' : fun },
  T.epunct  : { 'order' :  1, 'parse' : fun },
  T.mpunct  : { 'order' :  2, 'parse' : fun },
  T.decimal : { 'order' :  3, 'parse' : fun },
  T.punct   : { 'order' :  4, 'parse' : fun },
  T.capital : { 'order' :  5, 'parse' : fun },
  T.prefix  : { 'order' :  6, 'parse' : fun },
  T.abbrev  : { 'order' :  7, 'parse' : fun },
  T.wcell   : { 'order' :  8, 'parse' : fun },
  T.cluster : { 'order' :  9, 'parse' : fun },
  T.number  : { 'order' : 10, 'parse' : fun },
  T.letter  : { 'order' : 11, 'parse' : fun },
  T.nonlatin: { 'order' : 12, 'parse' : fun },
  T.char    : { 'order' : 13, 'parse' : fun },
  T.accent  : { 'order' : -1, 'parse' : fun },
  T.italic  : { 'order' : -1, 'parse' : fun },
  T.space   : { 'order' : -1, 'parse' : fun },
  T.unknown : { 'order' : -1, 'parse' : None },
}


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

'''
Final letter contractions - These are formed much as the initial letter
contractions, except that the prefix is followed by the final letter of
the expanded form, instead of the inital. Also, there are no final forms
using multiple letters, so no embedded counts are needed.
'''

'''
One cell words - A select few words can be contracted to a single
cell, with disambiguation left up to the reader. Since this can be
quite confusing, one might assume that these contractions cannot be used
within a word, as are the part-word contractions, defined below.
However, I have not found a rule for this, and at least some of these
abbreviations (e.g. X=it) are acceptable either as a separate word, or
as a part-word contraction.
'''

'''
One cell part-words - These contractions may occur as part of a word, or
as a stand-alone word. Most of these stand for consonant or vowel
clusters, but a few stand for some words which commonly occur as part of
a word or alone. These must be encoded directly to Braille, as we are at
the last stage of contraction, followed by simple one-to-one substitutions
(i.e. Grade 1 Braille.)
'''

def convert(line):
  '''
  converts a line of English (ASCII) text to Braille. For more
  information, consult the comments interspersed with the data
  structures, above.
  '''
  res = []

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
    #punctuation
    #opening quotes
    for (p, b) in st_punct:
      word = re.sub(r'^([^\w]*)%s(\W*\w+)' % p, r'\1%s\2' % b, word)

    #closing quotes
    for (p, b) in cl_punct:
      word = re.sub( r'(\w+\W*)%s(\W*)$' % p, r'\1%s\2' % b, word)

    #other punctuation
    for (p, b) in punctuation:
      word = word.replace(p,b)
	
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
      #print 'word, oc, sf: %s, %s, %s' % (word, oc, sf)
      word = re.sub(r'\b%s\b' % oc, sf, word)

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

    #letters
    for (c, b) in letters:
      word = word.replace(c, b)

    res.append(word)

  return ' '.join(res)



if __name__ == '__main__':
  oline = ""
  while (True):
    line = sys.stdin.readline()

    oline = convert(line)

    #Helps readability on monospace outputs--like a terminal
    oline = oline.replace('', ' ')

    print oline.strip()
    oline = ''
