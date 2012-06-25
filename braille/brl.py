# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''
High level functions for translation of English text to Braille.
'''

from .lang import import_ruleset
from . import ds
from .options import opt
from .util import fwarn, do_re, gettype

def _r_convert(line, lang='amer-2'):
  '''
  converts a line of English (ASCII) text to Braille. For more
  information, consult the comments interspersed with the data
  structures, above. Uses new rule-based mechanism: use
  convert_r(line, lang='...') to change the language rules used.
  '''
  rules = import_ruleset(lang)
  cxt = ds.Context()
  cxt.fname = '(str)'
  cxt.lineno = 0

  def match_rules(cxt, rules, word):

    #Don't bother with spaces
    if not word:
      return word
    #or with other whitespace
    if do_re(ds.patt.space, word):
      return word

    #Match rule
    for i in xrange(len(rules)):
      rule = rules[i]
      oword = word
      word = gettype(rule, 'trans')(rule, cxt, word)
      if opt('debug') and not oword == word:
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

