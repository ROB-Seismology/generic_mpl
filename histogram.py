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


def plot_histogram(datasets, bins, data_is_binned=False,
				histogram_type='bar', cumulative=False, stacked=True, normed=False,
				orientation='vertical', align='mid', bar_width=None, baseline=None,
				colors=[], labels=[],
				line_color='k', line_width=0.5,
				xscaling='lin', yscaling='lin',
				xmin=None, xmax=None, ymin=None, ymax=None,
				xlabel='', ylabel='N', ax_label_fontsize='large',
				xticks=None, xticklabels=None, xtick_interval=None, xtick_rotation=0,
				xtick_direction='', xtick_side='',
				yticks=None, yticklabels=None, ytick_interval=None, ytick_rotation=0,
				ytick_direction='', ytick_side='',
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
		list of 1-D arrays
	:param bins:
		int (number of bins) or list or array (bin edges)
	:param data_is_binned:
		bool, whether or not data in :param:`datasets` is already binned
		Note that, if this is True, :param:`bins` must correspond to
		the bin edges (including right edge)!
		(default: False)
	"""
	frame_args = {key: val for (key, val) in locals().items()
				if not key in ['datasets', 'bins', 'data_is_binned', 'histogram_type',
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
	if isinstance(colors, basestring):
		colors = matplotlib.cm.get_cmap(colors)
	if isinstance(colors, matplotlib.colors.Colormap):
		colors = colors(np.linspace(0, 1, len(datasets)))
	if not labels:
		labels = ['%d' % i for i in range(len(datasets))]
	unique_labels = set(labels)

	colors = cycle(colors)
	labels = cycle(labels)

	colors = [colors.next() for i in range(len(datasets))]
	labels = [labels.next() for i in range(len(datasets))]

	## Histogram
	if orientation == 'vertical' and 'log' in yscaling:
		log = True
	elif orientation == 'horizontal' and 'log' in xscaling:
		log = True
	else:
		log = False

	if data_is_binned:
		#The weights are the y-values of the input binned data
		weights = datasets
		#The dataset values are the bin centres
		bins = np.asarray(bins)
		datasets = [((bins[1:] + bins[:-1]) / 2.) for i in range(len(datasets))]
	else:
		weights = None

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
