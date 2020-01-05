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

## plot_generic
if not reloading:
  from . import plot_generic
else:
  reload(plot_generic)
from .plot_generic import *
