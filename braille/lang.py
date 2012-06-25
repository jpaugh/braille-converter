# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''
Functions that deal with lang files or rulesets
'''

import ds
import comp as cpl
from .options import opt
from .util import fwarn, do_re, gettype

import os

langdir = os.path.join(os.path.dirname(__file__), 'lang')
if not os.path.isdir(langdir):
  raise IOError('Cannot load lang files; unknown dir "%s"' % langdir)

#Cache of imported rulesets, indexed by lang name
ruleset = { }

def import_ruleset(lang='amer-2', comp=None, fresh=False):
  '''
  loads the rules for the given language

  params:
  -------
  lang='amer-2' Language to load. Defaults to American Grade 2.
    This consists of solely of alphanumeric characters and hyphens.

  comp=True - Compile the ruleset to the most succint form (brl).
    The default is set by commandline-argument.

  fresh=False - Get a fresh version of the ruleset, from file, rather
  than relying on the cache. Defaults False.
    If you change the comp option (or change the lang file), you must
    set this to True to see your changes.
  '''

  #Don't be grumpy about underscores.
  lang = lang.replace('_', '-')

  rules = []

  #prefer cached version first
  if not fresh and lang in ruleset:
    return ruleset[lang]

  #Set default comp
  if comp == None:
    comp = opt('comp')

  #Import standard (international) rules first
  if (not lang == 'standard' and
  not 'standard' in ruleset):
    import_ruleset('standard')

  cxt = ds.Context()
  cxt.fname = os.path.join(langdir, lang)
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
  rule = do_re(ds.patt.rule, line)
  if not rule:
    fwarn(cxt, 'Invalid Rule "%s"' % line)
    return None

  typ = rule['type'].lower()
  rule['type'] = typ
  if not typ in ds.types:
    fwarn(cxt, 'Unknown rule type: '+typ)
    return None

  if not rule['priority']:
    rule['priority'] = 1

  #Compile the rule. (Convert it's brl to minimum form)
  fun = gettype(rule, 'comp')
  if comp or fun == cpl.dotify or fun == cpl.prefix:
    fun(cxt, rule)
  else:
    #The minimum we must do is dotify any dots
    cpl.try_dotify(cxt, rule)

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
