from . import BrTestCase, dots

class Regressions(BrTestCase):
  def pairs(self):
    return (
	('was.', dots('356 256')),
	('but-this', dots('12 36 1456')),
	)

