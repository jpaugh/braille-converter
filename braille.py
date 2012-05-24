#!/usr/bin/env python
#to-braille - converts text to English Braile. encoding=utf8

import sys, re

stderr = sys.stderr

version = (0, 1, 1, 2002, 'beta')

ruleset = { }


class Context(object):
  '''
  Stores position info in a file or string source in an organised way.
  Generally useful for error messages (via fwarn).
  '''
  __slots__ = 'fname lineno pos'.split()


class T:
  '''
  Type enums - and some compound enums
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


class patt:
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

#Compilation identity
comp_ident = lambda c, r: r

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

def comp_prefix(cxt, rule):
  try_dotify(cxt, rule)
  fwarn(cxt, 'brl: "%s"' % rule['brl'])
  rule['brl'] = rule['brl'].replace(' ', '')
  fwarn(cxt, 'brl: "%s"' % rule['brl'])


#Identity - useful for unimplemented features
trans_ident = lambda r, c, w: w

trans_TODO = trans_ident

def trans_simple(rule, cxt, word):
  return word.replace(rule['prn'], rule['brl'])

def trans_wcell(rule, cxt, word):
  '''
  Only translate if it matches the whole word.
  '''
  if word == rule['prn']:
    return rule['brl']
  return word

def trans_capital(rule, cxt, word):
  '''
  Mark all capital letters as such.
  '''
  return patt.capital.sub(rule['brl'] + '\\1', word).lower()

def trans_letter(rule, cxt, word):
  '''
  Mark all words that are preceeded by a number.
  '''
  return patt.letter.sub('\\1%s\\2' % rule['brl'], word).lower()

def trans_number(rule, cxt, word):
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
  return patt.number.sub(repl, word)

def trans_decimal(rule, cxt, word):
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

def trans_bpunct(rule, cxt, word):
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

def trans_epunct(rule, cxt, word):
  ere = r'(\w+\W*)%s(\W*)$'
  esub = r'\1%s\2'

  try:
    return re.sub(ere % rule['prn'], esub % rule['brl'], word)
  except Exception as e:
    fwarn(cxt, e.message)
    return word

#Type info
#   order: sort order
#   reduce: fun to reduce the brl of any rule of this type
#   parse:  parsing strategy (function) for when this rule matches
types = {
  T.bpunct  : { 'order' :  0, 'comp' : dotify, 'trans' : trans_bpunct },
  T.epunct  : { 'order' :  1, 'comp' : dotify, 'trans' : trans_epunct },
  T.mpunct  : { 'order' :  2, 'comp' : dotify, 'trans' : trans_simple },
  T.decimal : { 'order' :  3, 'comp' : dotify, 'trans' : trans_decimal },
  T.punct   : { 'order' :  4, 'comp' : dotify, 'trans' : trans_simple },
  T.capital : { 'order' :  5, 'comp' : dotify, 'trans' : trans_capital },
  T.prefix  : { 'order' :  6, 'comp' : comp_prefix, 'trans' : trans_simple },
  T.abbrev  : { 'order' :  7, 'comp' : comp_ident, 'trans' : trans_simple },
  T.wcell   : { 'order' :  8, 'comp' : comp_ident, 'trans' : trans_wcell },
  T.cluster : { 'order' :  9, 'comp' : dotify, 'trans' : trans_simple },
  T.number  : { 'order' : 10, 'comp' : dotify, 'trans' : trans_number },
  T.letter  : { 'order' : 11, 'comp' : dotify, 'trans' : trans_letter },
  T.nonlatin: { 'order' : 12, 'comp' : dotify, 'trans' : trans_ident },
  T.char    : { 'order' : 13, 'comp' : dotify, 'trans' : trans_simple },
  T.accent  : { 'order' : -1, 'comp' : dotify, 'trans' : trans_ident },
  T.italic  : { 'order' : -1, 'comp' : dotify, 'trans' : trans_ident },
  T.space   : { 'order' : -1, 'comp' : comp_ident, 'trans' : trans_ident },
  T.unknown : { 'order' : -1, 'comp' : comp_ident, 'trans' : trans_ident },
}


def warn(msg):
  '''
  Give a warning to the user on stderr
  '''
  print >>stderr, msg
  sys.stderr.flush()

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
    return types[typ]
  else:
    return types[typ][key]

def import_ruleset(lang='amer-2', comp=False, fresh=False):
  '''
  loads the rules for the given language

  params:
  comp=False - Do not compile the ruleset This is for easier debugging,
  but gives a slower runtime

  fresh=False - Use cached version, instead of regenerating every time.
  If you change comp (or change a file), you must set this to True for
  it to take effect.
  '''
  lang = lang.replace('_', '-')
  rules = []

  #prefer cached version first
  if not fresh and lang in ruleset:
    return ruleset[lang]

  #Import standard (international) rules first
  if (not lang == 'standard' and
  not 'standard' in ruleset):
    import_ruleset('standard')

  cxt = Context()
  import os
  cxt.fname = os.path.join('lang', lang)
  cxt.lineno = 0

  try:
    with open(cxt.fname) as lfile:
      for line in lfile:
	cxt.lineno += 1
	rule = __parse_rule(cxt, line, comp)
	if rule:
	  rules.append(rule)
  except IOError as e:
    raise

  rules.sort(cmp=__cmp_rules)
  # cache ruleset for this language
  ruleset[lang] = rules

  if not lang == 'standard':
    rules.extend(ruleset['standard'])
  return rules

def __parse_rule(cxt, line, comp=False):
  '''
  parse a string into a line tuple.
  '''
  line = line.strip()
  if (not line) or line[0] == '#':
    return None
  rule = do_re(patt.rule, line)
  if not rule:
    fwarn(cxt, 'Invalid Rule "%s"' % line)
    return None

  typ = rule['type'].lower()
  rule['type'] = typ
  if not typ in types:
    fwarn(cxt, 'Unknown rule type: '+typ)
    return None

  if not rule['priority']:
    rule['priority'] = 1

  #Compile the rule. (Convert it's brl to minimum form)
  fun = gettype(rule, 'comp')
  if comp or fun == dotify or fun == comp_prefix:
    fun(cxt, rule)
  else:
    #The minimum we must do is dotify any dots
    try_dotify(cxt, rule)

  return rule


def __cmp_rules(x, y):
  '''
  cmp function for the rules.
  '''
  if gettype(x, 'order') < gettype(y, 'order'):
    return -1
  elif gettype(x, 'order') > gettype(y, 'order'):
    return 1
  elif x['priority'] < y['priority']:
    return -1
  elif x['priority'] > y['priority']:
    return 1
  else:
    # Longer strings first
    return -1 * cmp(len(x['prn']), len(y['prn']))


def __dot(s):
  '''
  helper for dots()

  Does not expect multiple characters in one string.
  DOES work for 8bit dots (i.e. European Braille).
  '''
  if not s.isdigit():
    raise ValueError('Invalid dot pattern: "%s"' % s)
  num = 0x2800
  for n in (1,2,3,4,5,6,7,8):
    if str(n) in s:
      num |= 2**(n-1)

  return unichr(num)


def dots(s):
  '''
  convert a sequence of Braille dot patterns (string) to the
  corresponding Braille characters.

  NOTE: The dots for each cell must be separated by a single space. To
  include a literal space, use two dots instead.
  '''
  res = ''
  for word in s.split(' '):
    if word:
      res += __dot(word)
    else: # empty string means add a space
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
output of __dot() is a string, and how the arithmetic operators work for
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

def _r_convert(line, lang='amer-2'):
  '''
  converts a line of English (ASCII) text to Braille. For more
  information, consult the comments interspersed with the data
  structures, above. Uses new rule-based mechanism: use
  convert_r(line, lang='...') to change the language rules used.
  '''
  rules = import_ruleset(lang)
  cxt = Context()
  cxt.fname = '(str)'
  cxt.lineno = 0

  def match_rules(cxt, rules, word):

    #Don't bother with spaces
    if not word:
      return word
    #or with other whitespace
    if do_re(patt.space, word):
      return word

    #Match rule
    for i in xrange(len(rules)):
      rule = rules[i]
      oword = word
      word = gettype(rule, 'trans')(rule, cxt, word)
      if not oword == word:
	fwarn(cxt, '%s --> %s by rule %d (%s)' % (oword, word, i, rule))
    return word

  words = [ match_rules(cxt, rules, w)
      for w in line.split(' ') ]

  return ' '.join(words)

convert = _r_convert

def __old_convert(line):
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
