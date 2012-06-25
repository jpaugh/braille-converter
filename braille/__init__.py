# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''   coding=utf8
braille converter

Convert text to braille
'''


import sys, re

version = (1, 3, 2002)

import ds, util, options
from .lang import import_ruleset
from .util import dots, gettype, warn, fwarn
from .brl import convert
from .options import opt





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
