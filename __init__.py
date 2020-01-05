"""
Generic plot functions based on matplotlib
"""

from __future__ import absolute_import, division, print_function, unicode_literals


## Reloading mechanism
try:
	reloading
except NameError:
	## Module is imported for the first time
	reloading = False
else:
	## Module is reloaded
	reloading = True
	try:
		## Python 3
		from importlib import reload
	except ImportError:
		## Python 2
		pass


## Import submodules

## common (no internal dependencies)
if not reloading:
	from . import common
else:
	reload(common)
from .common import *

## frame (no internal dependencies)
if not reloading:
	from . import frame
else:
	reload(frame)
from .frame import *

## xy (depends on common, frame)
if not reloading:
	from . import xy
else:
	reload(xy)
from .xy import *

## histogram (depends on common, frame)
if not reloading:
	from . import histogram
else:
	reload(histogram)
from .histogram import *

## grid (depends on common, frame)
if not reloading:
	from . import grid
else:
	reload(grid)
from .grid import *
