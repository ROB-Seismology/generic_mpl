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
import numpy as np
import pylab
import matplotlib
from matplotlib.font_manager import FontProperties


from .common import (show_or_save_plot, common_doc)
from .frame import (plot_ax_frame, ax_frame_doc)


__all__ = ['plot_histogram']


def plot_histogram(datasets, bins, data_is_binned=False, weights=None,
				histogram_type='bar', stacked=True, cumulative=False, normed=False,
				orientation='vertical', align='mid', bar_width=0.8, baseline=0,
				colors=[], labels=[],
				line_color='k', line_width=0.5,
				xscaling='lin', yscaling='lin',
				xmin=None, xmax=None, ymin=None, ymax=None,
				xlabel='', ylabel='N', ax_label_fontsize='large',
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
	Plot histograms

	:param datasets:
		list of 1-D arrays, datasets containing either data to be
		binned or counts, (i.e., data that is already binned,
		see :param:`data_is_binned`)
	:param bins:
		int (number of bins) or list or array (bin edges)
	:param data_is_binned:
		bool, whether or not data in :param:`datasets` is already binned
		Note that, if this is True, :param:`bins` must correspond to
		the bin edges (including right edge)!
		(default: False)
	:param weights:
		array with same shape as :param:`datasets`, weights associated
		with each value. Only applies if :param:`data_is_binned` is False
		(default: None)
	:param histogram_type:
		str, histogram type: 'bar', 'step' or 'stepfilled'
		(default: 'bar')
	:param stacked:
		bool, whether to plot mulitple datasets on top of each other
		(True) or side by side (if :param:`histogram_type` is 'bar')
		or on top of each other (if :param:`histogram_type` is 'step')
		(default: True)
	:param cumulative:
		bool, whether or not to draw a cumulative histogram, where each
		bin gives the counts in that bin plus all bins for smaller values
		(default: False)
	:param normed:
		bool, whether or not counts should be normalized to sum to 1
		(default: False)
	:param orientation:
		str, orientation of histogram bars: 'horizontal' or 'vertical'
		(default: 'vertical')
	:param align:
		str, alignment of histogram bars: 'left', 'mid' or 'right'
		(default: 'mid')
	:param bar_width:
		float, relative width of bars as a fraction of the bin width
		(default: 0.8)
	:param baseline:
		float or array, location of the bottom baseline of each bin
		if array, its length must match the number of bins
		(default: 0)
	:param colors:
		list of matplotlib color specifications, one for each dataset
		or one for each bin if there is only 1 dataset
		May also be a matplotlib colormap or a string (colormap name)
		(default: [], will use default color(s))
	:param labels:
		list of strings, legend labels for each dataset
		(default: [], will not plot any labels)
	:param line_color:
		matplotlib color specification, color(s) of bar edges
		(default: 'k')
	:param line_width:
		float, width of bar edges
		(default: 0.5)
	"""
	frame_args = {key: val for (key, val) in locals().items()
				if not key in ['datasets', 'bins', 'data_is_binned',
							'weights', 'histogram_type',
							'cumulative', 'stacked', 'normed', 'orientation',
							'align', 'bar_width', 'baseline', 'colors', 'labels',
							'line_color', 'line_width',
							'legend_location', 'legend_fontsize', 'style_sheet',
							'border_width', 'skip_frame', 'fig_filespec',
							'figsize', 'dpi', 'ax']}

	from itertools import cycle

	pylab.style.use(style_sheet)

	if ax is None:
		fig, ax = pylab.subplots(figsize=figsize)
	else:
		fig = ax.get_figure()

	## markers, colors, linewidhts, linestyles, labels, etc.
	if not colors:
		#colors = 'bgrcmyk'
		colors = pylab.rcParams['axes.prop_cycle'].by_key()['color']
		colors = colors[:len(datasets)]
	if isinstance(colors, basestring):
		colors = matplotlib.cm.get_cmap(colors)
	if isinstance(colors, matplotlib.colors.Colormap):
		if len(datasets) > 1:
			num_colors = len(datasets)
		else:
			if np.isscalar(bins):
				num_colors = bins
			else:
				num_colors = len(bins) - 1
		dc = 1. / num_colors / 2.
		colors = colors(np.linspace(dc, 1-dc, num_colors))
	if not labels:
		#labels = ['%d' % i for i in range(len(datasets))]
		labels = [''] * len(datasets)
	unique_labels = set(labels)

	if not (len(datasets) == 1 and len(colors) > 1):
		colors = cycle(colors)
		colors = [next(colors) for i in range(len(datasets))]

	labels = cycle(labels)
	labels = [next(labels) for i in range(len(datasets))]

	## Histogram
	if orientation == 'vertical' and 'log' in yscaling:
		log = True
	elif orientation == 'horizontal' and 'log' in xscaling:
		log = True
	else:
		log = False

	if len(datasets) == 1 and len(colors) > 1 and histogram_type[:3] == 'bar':
		if not data_is_binned:
			bar_heights, bin_edges = pylab.histogram(datasets[0], bins=bins,
												normed=normed, weights=weights)
		else:
			bin_edges = bins
			bar_heights = datasets[0]

		if cumulative:
			bar_heights = np.cumsum(bar_heights)
			if normed:
				bar_heights /= bar_heights[-1]
		elif normed:
			bar_heights /= np.sum(bar_heights)

		if bar_width is None:
			bar_width = 0.8
		## Convert to absolute bar width, assuming uniform bin intervals
		bar_width *= np.abs(bin_edges[1] - bin_edges[0])

		if align == 'mid':
			align = 'center'
		elif align == 'left':
			align = 'edge'
		elif align == 'right':
			align = 'edge'
			bar_width = -bar_width

		ax.bar(bin_edges[:-1], bar_heights, width=bar_width, bottom=baseline,
				color=colors, edgecolor=line_color, linewidth=line_width,
				align=align, orientation=orientation, label=labels[0], log=log)
	else:
		if data_is_binned:
			#The weights are the y-values of the input binned data
			weights = datasets
			#The dataset values are the bin centres
			bins = np.asarray(bins)
			datasets = [((bins[1:] + bins[:-1]) / 2.) for i in range(len(datasets))]

		if align == 'center':
			align = 'mid'

		## Work around bug
		if np.isscalar(baseline):
			baseline = [baseline]

		ax.hist(datasets, bins, normed=normed, cumulative=cumulative,
				histtype=histogram_type, align=align, orientation=orientation,
				rwidth=bar_width, color=colors, label=labels, stacked=stacked,
				edgecolor=line_color, linewidth=line_width, bottom=baseline,
				log=log, weights=weights)

	## Frame
	if not skip_frame:
		plot_ax_frame(ax, **frame_args)

	## Legend
	legend_fontsize = legend_fontsize or tick_label_fontsize
	legend_font = FontProperties(size=legend_fontsize)
	## Avoid warning if there are no labeled curves
	if len(unique_labels.difference(set(['_nolegend_']))):
		ax.legend(loc=legend_location, prop=legend_font)

	## Output
	return show_or_save_plot(ax, fig_filespec=fig_filespec, dpi=dpi,
							border_width=border_width)

	## Restore default style if we get here
	pylab.style.use('default')

plot_histogram.__doc__ += (ax_frame_doc + common_doc)
