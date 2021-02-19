# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 12:32:32 2021

@author: kris
"""

from __future__ import absolute_import, division, print_function, unicode_literals



_all__ = ['get_random_colors', 'get_spaced_colors']


def get_random_colors(num_colors, color_table='css4', random_seed=None):
	"""
	Fetch random colors from one of the matplotlib color tables

	:param num_colors:
		int, number of random colors
	:param color_table:
		str, name of matplotlib color table: 'css4' or 'xkcd'
		- 'css4': HTML colors (148)
		- 'xkcd': most common RGB colors (949)
		(default: 'css4')
	:param random_seed:
		int, seed for random number generator
		(default: None)

	:return:
		list of strings (hex colors)
	"""
	import numpy as np

	if color_table.upper() == 'CSS4':
		from matplotlib.colors import CSS4_COLORS as COLOR_TABLE
	elif color_table.upper() == 'XKCD':
		from matplotlib.colors import XKCD_COLORS as COLOR_TABLE

	all_colors = list(COLOR_TABLE.values())
	np.random.seed(random_seed)
	random_color_idxs = np.random.choice(len(COLOR_TABLE), num_colors,
													replace=False)
	sampled_colors = [all_colors[idx] for idx in random_color_idxs]

	return sampled_colors


def get_spaced_colors(num_colors, color_table='css4'):
	"""
	Fetch more or less equally spaced colors from one of the matplotlib
	color tables

	:param num_colors:
		int, number of random colors
	:param color_table:
		str, name of matplotlib color table: 'css4' or 'xkcd'
		- 'css4': HTML colors (148)
		- 'xkcd': most common RGB colors (949)
		(default: 'css4')

	:return:
		list of strings (hex colors)
	"""
	import numpy as np

	if color_table.upper() == 'CSS4':
		from matplotlib.colors import CSS4_COLORS as COLOR_TABLE
	elif color_table.upper() == 'XKCD':
		from matplotlib.colors import XKCD_COLORS as COLOR_TABLE

	all_colors = list(COLOR_TABLE.values())
	len_color_table = len(all_colors)
	step = float(len_color_table) / num_colors / 2.
	color_idxs = np.arange(0, len_color_table-0.1, step)
	color_idxs = np.round(color_idxs)

	spaced_colors = [all_colors[int(idx)] for idx in color_idxs]

	return spaced_colors
