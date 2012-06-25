# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''
Package-wide settings defined all in one place.

WARNING: For this to work, every import of this module MUST use the same name:
  import braille.settings
  from . import settings
  from .settings import option

NOTE: This module may NOT rely on (import) other modules within the
package.
'''
import sys

#XXX Do NOT import this field! (use the accessor methods, below)
__option = {
    'gui': True,
    'debug': False,
    'comp': True, #Currently a no-op
    'stdin': sys.stdin,
    'stdout': sys.stdout,
    'stderr': sys.stderr,
    'logger': None,
    }

def opt(name, value=None):
  '''
  Get or set the value of an option by name. In any wise, the return
  value is the value of the option.
  '''
  if not name in __option:
    raise ValueError, 'key %s not found in options' % name

  if value:
    __option[name] = value

  return __option[name]

def override(new_opts=None):
  if not new_opts:
    raise ValueError, 'new_opts should be a suitable dict object'

  __option.update(new_opts)
