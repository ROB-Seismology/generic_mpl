"""
Generic plot functions based on matplotlib
"""

from __future__ import absolute_import, division, print_function, unicode_literals

try:
	## Python 2
	basestring
except:
	## Python 3
	basestring = str

import datetime

import numpy as np
import pylab
import matplotlib
from matplotlib.font_manager import FontProperties

from .common import (show_or_save_plot, common_doc)
from .frame import (plot_ax_frame, ax_frame_doc)


__all__ = ['plot_xy', 'plot_density']


def plot_xy(datasets,
			colors=[], fill_colors=[], linewidths=[1], linestyles=['-'], labels=[],
			markers=[], marker_sizes=[6], marker_intervals=[],
			marker_edge_colors=['k'], marker_fill_colors=[], marker_edge_widths=[1],
			marker_labels=[], marker_label_fontsize='small',
			xscaling='lin', yscaling='lin',
			xmin=None, xmax=None, ymin=None, ymax=None,
			xlabel='', ylabel='', ax_label_fontsize='large',
			xticks=None, xtick_labels=None, xtick_interval=None, xtick_rotation=0,
			xtick_direction='', xtick_side='', xlabel_side='',
			yticks=None, ytick_labels=None, ytick_interval=None, ytick_rotation=0,
			ytick_direction='', ytick_side='', ylabel_side='',
			tick_label_fontsize='medium', tick_params={},
			title='', title_fontsize='large',
			xgrid=0, ygrid=0, aspect_ratio=None,
			hlines=[], hline_args={}, vlines=[], vline_args={},
			legend_location=0, legend_fontsize='medium',
			style_sheet='classic', border_width=0.2, skip_frame=False,
			fig_filespec=None, figsize=None, dpi=300, ax=None):
	"""
	Generic function to plot (X, Y) data sets (lines, symbols and/or polygons)

	:param datasets:
		list with (x, y) array tuples (either values or datetimes)
	:param colors:
		list of line colors to cycle over for each dataset
		or instance of :class:`matplotlib.colors.Colormap`
		(default: [], will use default colors for :param:`style_sheet`)
	:param fill_colors:
		list of fill colors to cycle over for each dataset
		(default: [], will not apply fill color)
	:param linewidths:
		list of line widths to cycle over for each dataset
		(default: [1])
	:param linestyles:
		list of line styles to cycle over for each dataset
		(default: ['-'])
	:param labels:
		list of labels to cycle over for each dataset
		(default: [], will not label curves)
	:param markers:
		list of marker symbols to cycle over for each dataset
		(default: [], will not draw markers)
	:param marker_sizes:
		list of marker sizes to cycle over for each dataset
		May also be a list of arrays with variable sizes for each point
		in dataset if linestyle for this dataset is empty or linewidth
		is zero
		(default: [6])
	:param marker_intervals:
		(default: [], will draw marker for each datapoint)
	:param marker_edge_colors:
		list of marker line colors to cycle over for each dataset
		May also be a list of color lists with variable colors for each
		point in dataset if linestyle for this dataset is empty or
		linewidth is zero
		(default: ['k'])
	:param marker_fill_colors:
		list of marker fill colors to cycle over for each dataset
		May also be a list of color lists with variable colors for each
		point in dataset if linestyle for this dataset is empty or
		linewidth is zero
		(default: [], will use colors defined in :param:`colors`)
	:param marker_edge_widths:
		list of marker line widths to cycle over for each dataset
		(default: [1])
	"""
	frame_args = {key: val for (key, val) in locals().items()
				if not key in ['datasets', 'colors', 'fill_colors', 'linewidths',
							'linestyles', 'labels', 'markers', 'marker_sizes',
							'marker_intervals', 'marker_edge_colors',
							'marker_fill_colors', 'marker_edge_widths',
							'marker_labels', 'marker_label_fontsize',
							'legend_location', 'legend_fontsize', 'style_sheet',
							'border_width', 'skip_frame', 'fig_filespec',
							'figsize', 'dpi', 'ax']}

	from itertools import cycle

	pylab.style.use(style_sheet)

	if ax is None:
		#ax = pylab.axes()
		fig, ax = pylab.subplots(figsize=figsize, facecolor='white')
	else:
		fig = ax.get_figure()

	## markers, colors, linewidhts, linestyles, labels, etc.
	if not colors:
		#colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
		#colors = 'bgrcmyk'
		colors = pylab.rcParams['axes.prop_cycle'].by_key()['color']
	if isinstance(colors, basestring):
		colors = matplotlib.cm.get_cmap(colors)
	if isinstance(colors, matplotlib.colors.Colormap):
		colors = colors(np.linspace(0, 1, len(datasets)))
	if not fill_colors:
		fill_colors = [None]
	if linewidths is None or linewidths == []:
		linewidths = [1]
	if not linestyles:
		linestyles = ['-']
	if not markers:
		markers = ['']
	if marker_sizes is None or marker_sizes == []:
		marker_sizes = [6]
	if not marker_intervals:
		marker_intervals = [None]
	if not marker_edge_colors:
		marker_edge_colors = ['k']
	if not marker_fill_colors:
		marker_fill_colors = colors[:]
	if not marker_edge_widths:
		marker_edge_widths = [1]
	if not labels:
		labels = ['_nolegend_']
	unique_labels = set(labels)

	colors = cycle(colors)
	fill_colors = cycle(fill_colors)
	linewidths = cycle(linewidths)
	linestyles = cycle(linestyles)
	markers = cycle(markers)
	marker_sizes = cycle(marker_sizes)
	marker_intervals = cycle(marker_intervals)
	marker_edge_colors = cycle(marker_edge_colors)
	marker_fill_colors = cycle(marker_fill_colors)
	marker_edge_widths = cycle(marker_edge_widths)
	labels = cycle(labels)

	#if xscaling == 'lin':
	#	if yscaling == 'lin':
	#		plotfunc = getattr(ax, 'plot')
	#	elif yscaling == 'log':
	#		plotfunc = getattr(ax, 'semilogy')
	#elif xscaling == 'log':
	#	if yscaling == 'lin':
	#		plotfunc = getattr(ax, 'semilogx')
	#	elif yscaling == 'log':
	#		plotfunc = getattr(ax, 'loglog')

	for (x, y) in datasets:
		assert len(x) == len(y)
		color = next(colors)
		fill_color = next(fill_colors)
		linewidth = next(linewidths)
		linestyle = next(linestyles)
		marker = next(markers)
		marker_size = next(marker_sizes)
		marker_interval = next(marker_intervals)
		marker_edge_color = next(marker_edge_colors)
		marker_fill_color = next(marker_fill_colors)
		marker_edge_width = next(marker_edge_widths)
		label = next(labels)

		if len(x) == 0:
			continue

		if isinstance(x[0], datetime.datetime):
			## Doesn't seem to be necessary
			#x = pylab.date2num(x)
			x_is_date = True
		else:
			x_is_date = False
		if isinstance(y[0], datetime.datetime):
			#y = pylab.date2num(y)
			y_is_date = True
		else:
			y_is_date = False

		if fill_color:
			ax.fill(x, y, facecolor=fill_color, edgecolor=color, lw=linewidth,
				ls=linestyle, label=label)
			if marker:
				ax.plot(x, y, marker, lw=0, ms=marker_size, mec=marker_edge_color,
				mfc=marker_fill_color, mew=marker_edge_width, markevery=marker_interval,
				label='_nolegend_')
		else:
			#if not (np.isscalar(marker_size) and np.isscalar(marker_edge_color)
			#		and np.isscalar(marker_fill_color)):
			if linestyle in ('', 'none', 'None') or linewidth == 0:
				## No line, marker sizes and/or colors may be different
				ax.scatter(x, y, s=np.power(marker_size, 2), edgecolors=marker_edge_color,
					marker=marker, facecolors=marker_fill_color, linewidth=marker_edge_width,
					label=label)
			else:
				## Markers are associated with lines and should have same size/color
				ax.plot(x, y, marker, color=color, ls=linestyle, lw=linewidth,
					ms=marker_size, mec=marker_edge_color, mfc=marker_fill_color,
					mew=marker_edge_width, markevery=marker_interval, label=label)

		for i, lbl in enumerate(marker_labels):
			ax.annotate(lbl, (x[i], y[i]), fontsize=marker_label_fontsize,
							clip_on=True)

	## Frame
	if not skip_frame:
		plot_ax_frame(ax, x_is_date=x_is_date, y_is_date=y_is_date, **frame_args)

	## Legend
	legend_fontsize = legend_fontsize or tick_label_fontsize
	legend_font = FontProperties(size=legend_fontsize)
	## Avoid warning if there are no labeled curves
	if len(unique_labels.difference(set(['_nolegend_', '']))):
		ax.legend(loc=legend_location, prop=legend_font)

	#if fig and tight_layout:
	#	fig.tight_layout(pad=0)

	## Output
	return show_or_save_plot(ax, fig_filespec=fig_filespec, dpi=dpi,
							border_width=border_width)

	## Restore default style if we get here
	pylab.style.use('default')

plot_xy.__doc__ += (ax_frame_doc + common_doc)


def plot_density(x, y, grid_size, density_type='hist2d', min_cnt=None, max_cnt=None,
			bins=None, cmap='plasma', cbar_args={}, cbar_label='N',
			xscaling='lin', yscaling='lin',
			xmin=None, xmax=None, ymin=None, ymax=None,
			xlabel='', ylabel='', ax_label_fontsize='large',
			xticks=None, xtick_labels=None, xtick_interval=None, xtick_rotation=0,
			xtick_direction='', xtick_side='', xlabel_side='',
			yticks=None, ytick_labels=None, ytick_interval=None, ytick_rotation=0,
			tick_label_fontsize='medium', tick_params={},
			ytick_direction='', ytick_side='', ylabel_side='',
			xgrid=0, ygrid=0, aspect_ratio=None,
			hlines=[], hline_args={}, vlines=[], vline_args={},
			title='', title_fontsize='large',
			style_sheet='classic', border_width=0.2, skip_frame=False,
			fig_filespec=None, figsize=None, dpi=300, ax=None):
	"""
	Plot XY data as density (number of data points per grid cell)

	:param x:
		1-D array, X data
	:param y:
		1-D array, Y data
	:param grid_size:
		int or (int, int) tuple, the number of grid cells in the X/Y
		direction
	:param density_type:
		str, type of density plot: 'hist2d', 'hexbin' or 'kde'
		(default: 'hist2d')
	:param min_cnt:
		int, minimum density to plot
		(default: None)
	:param max_cnt:
		int, maximum density to plot
		(default: None)
	:param bins:
		None, 'log' or list or array with bin edges, density bins
		(default: None)
	:param cmap:
		str or matplotlib Colormap object, colormap
		(default: 'plasma')
	:param cbar_args:
		dict, arguments to pass to :func:`matplotlib.colorbar`
	:param cbar_label:
		str, colorbar label
		(default: 'N')
	"""
	frame_args = {key: val for (key, val) in locals().items()
				if not key in ['x', 'y', 'grid_size', 'density_type',
							'min_cnt', 'max_cnt', 'cmap', 'bins', 'cbar_args',
							'cbar_label', 'style_sheet', 'border_width',
							'skip_frame', 'fig_filespec', 'figsize', 'dpi', 'ax']}

	pylab.style.use(style_sheet)

	if ax is None:
		#ax = pylab.axes()
		fig, ax = pylab.subplots(figsize=figsize, facecolor='white')
	else:
		fig = ax.get_figure()

	## Density plot
	if isinstance(grid_size, int):
		grid_size = (grid_size, grid_size)

	if cmap is None:
		cmap = pylab.rcParams['image.cmap']
	if not isinstance(cmap, matplotlib.colors.Colormap):
		cmap = pylab.cm.get_cmap(cmap)
	cmap.set_bad((1,1,1,0))
	cmap.set_under((1,1,1,0))

	nan_idxs = np.isnan(x) | np.isnan(y)
	x, y = x[~nan_idxs], y[~nan_idxs]

	_xmin = xmin if xmin is not None else x.min()
	_xmax = xmax if xmax is not None else x.max()
	_ymin = ymin if ymin is not None else y.min()
	_ymax = ymax if ymax is not None else y.max()

	if density_type == 'hist2d':
		range = [[_xmin, _xmax], [_ymin, _ymax]]
		if bins is None:
			#norm = None
			norm = matplotlib.colors.Normalize(vmin=min_cnt, vmax=max_cnt)
		elif bins == 'log':
			norm = matplotlib.colors.LogNorm()
		else:
			from mapping.layeredbasemap.cm.norm import PiecewiseLinearNorm
			norm = PiecewiseLinearNorm(bins)
		_, _, _, sm = ax.hist2d(x, y, bins=grid_size, range=range, cmap=cmap,
								cmin=min_cnt, cmax=max_cnt, norm=norm)

	elif density_type == 'hexbin':
		extent = (_xmin, _xmax, _ymin, _ymax)
		sm = ax.hexbin(x, y, gridsize=grid_size, cmap=cmap, bins=bins,
						mincnt=min_cnt, extent=extent)

	elif density_type == 'kde':
		from scipy.stats import kde
		k = kde.gaussian_kde([x, y])
		xi, yi = np.mgrid[_xmin: _xmax: grid_size[0]*1j, _ymin: _ymax: grid_size[1]*1j]
		zi = k(np.vstack([xi.flatten(), yi.flatten()]))
		## Un-normalize density
		zi *= (float(len(x)) / np.sum(zi))
		extent = (_xmin, _xmax, _ymin, _ymax)
		if bins is None:
			#norm = None
			norm = matplotlib.colors.Normalize(vmin=min_cnt, vmax=max_cnt)
		elif bins == 'log':
			norm = matplotlib.colors.LogNorm()
		else:
			from mapping.layeredbasemap.cm.norm import PiecewiseLinearNorm
			norm = PiecewiseLinearNorm(bins)
		sm = ax.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=cmap, norm=norm)
		ax.axis(extent)

	## Frame
	if not skip_frame:
		if isinstance(x[0], datetime.datetime):
			x_is_date = True
		else:
			x_is_date = False
		if isinstance(y[0], datetime.datetime):
			y_is_date = True
		else:
			y_is_date = False
		plot_ax_frame(ax, x_is_date=x_is_date, y_is_date=y_is_date, **frame_args)

	## Colorbar
	cbar = pylab.colorbar(sm, ax=ax, **cbar_args)
	cbar.set_label(cbar_label)

	## Output
	return show_or_save_plot(ax, fig_filespec=fig_filespec, dpi=dpi,
							border_width=border_width)

	## Restore default style if we get here
	pylab.style.use('default')

plot_density.__doc__ += (ax_frame_doc + common_doc)
