'''
Package-wide settings defined all in one place.

WARNING: For this to work, every import of this module MUST use the same name:
  import braille.settings
  from . import settings
  from .settings import option

NOTE: This module may NOT rely on (import) other modules within the
package.
'''

#XXX Do NOT import this field! (use the accessor methods, below)
__option = {
    'debug': False,
    'comp': True, #Currently a no-op
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
