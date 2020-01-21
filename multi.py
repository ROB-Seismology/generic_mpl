"""
Multi-plot with rows and columns
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import int

try:
	## Python 2
	basestring
except:
	## Python 3
	basestring = str

import matplotlib
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import AnchoredText
import pylab



__all__ = ['create_multi_plot']


def create_multi_plot(num_rows, num_cols, wspace=None, hspace=None,
					width_ratios=None, height_ratios=None,
					labels=[], label_font='large', label_loc='upper right',
					xmin=None, xmax=None, ymin=None, ymax=None,
					xtick_direction='', xtick_side='', xlabel_side='',
					ytick_direction='', ytick_side='', ylabel_side='',
					sharex=None, share_xlabel=True,
					sharey=None, share_ylabel=True,
					xlabel=None, ylabel=None, ax_label_font='large',
					col_titles=[], row_titles=[], col_row_title_font='large',
					hide_axes=False,
					title=None, title_font='x-large',
					ax_size=None, dpi=None):
	"""
	Create multi-plot or panel plot with plots organized in rows and columns

	fig.axes[col + row*num_cols]

	:param num_rows:
		int, number of rows
	:param num_cols:
		int, number of columns
	:param wspace:
		float, fraction of figure width to use for space between columns
		(default: None)
	:param hspace:
		float, fraction of figure height to use for space between rows
		(default: None)
	:param width_ratios:
		list of floats, relative width ratios of different columns
		(default: None)
	:param height_ratios:
		list of floats, relative height ratios of different rows
		(default: None)
	:param labels:
		list of strings, panel labels
		(default: [])

	"""
	# TODO: figsize or ax_size, aspect_ratio
	# TODO: style_sheet
	#fig = pylab.figure(constrained_layout=True)
	if ax_size:
		w, h = ax_size
		figsize = (w * num_cols, h * num_rows)
	else:
		figsize = None
	fig = pylab.figure(figsize=figsize, dpi=dpi)
	gs = gridspec.GridSpec(ncols=num_cols, nrows=num_rows,
						wspace=wspace, hspace=hspace,
						width_ratios=width_ratios, height_ratios=height_ratios)

	for row in range(num_rows):
		for col in range(num_cols):
			## Note: in newer version of matplotlib, it is possible to add
			## sharex/sharey arguments here. However, we do it manually below
			ax = fig.add_subplot(gs[row, col])

			if labels:
				i = row * num_cols + col
				try:
					label = labels[i]
				except IndexError:
					label = ''
				if isinstance(label_font, (int, basestring)):
					txt_kwargs = dict(prop={'fontsize': label_font})
				else:
					txt_kwargs = label_font.to_kwargs()
				txt = AnchoredText(label, loc=label_loc, **txt_kwargs)
				txt.set_zorder(10000)
				ax.add_artist(txt)

			## Ticks
			if xtick_direction:
				ax.tick_params(axis='x', direction=xtick_direction)

			if xtick_side:
				side_kwargs = {}
				if xtick_side in ('bottom', 'both'):
					side_kwargs['bottom'] = True
				if xtick_side in ('top', 'both'):
					side_kwargs['top'] = True
				if xtick_side == 'none':
					side_kwargs['top'] = side_kwargs['bottom'] = False
				ax.tick_params(axis='x', **side_kwargs)

			if ytick_direction:
				ax.tick_params(axis='y', direction=ytick_direction)

			if ytick_side:
				side_kwargs = {}
				if ytick_side in ('left', 'both'):
					side_kwargs['left'] = True
				if ytick_side in ('right', 'both'):
					side_kwargs['right'] = True
				if ytick_side == 'none':
					side_kwargs['left'] = side_kwargs['right'] = False
				ax.tick_params(axis='y', **side_kwargs)

			## Column / row labels
			if ax.is_first_row() and col < len(col_titles):
				#ax.set_title(col_titles[col], fontsize=col_row_title_font)
				if isinstance(col_row_title_font, (int, basestring)):
					txt_kwargs = dict(prop={'fontsize': col_row_title_font})
				else:
					txt_kwargs = col_row_title_font.to_kwargs()
				txt_kwargs.pop('rotation', None)
				txt = AnchoredText(col_titles[col], loc=8, frameon=True,
									bbox_to_anchor=(0.5, 1.),
									bbox_transform=ax.transAxes, **txt_kwargs)
				ax.add_artist(txt)
			if ax.is_first_col() and row < len(row_titles):
				if isinstance(col_row_title_font, (int, basestring)):
					txt_kwargs = dict(fontsize=col_row_title_font)
				else:
					txt_kwargs = col_row_title_font.to_kwargs()
				txt_kwargs['rotation'] = 90
				if not 'bbox' in txt_kwargs:
					txt_kwargs['bbox'] = dict(boxstyle='square', fc='w')
				txt_kwargs['va'] = 'center'
				txt_kwargs['ha'] = 'right'
				ax.annotate(row_titles[row], xy=(0., 0.5), xycoords='axes fraction',
							xytext=(-10, 0), textcoords='offset points',
							**txt_kwargs)
				"""
				## Note: AnchoredText does not support rotation
				txt_kwargs.pop('rotation', None)
				txt = AnchoredText(row_titles[row], loc=8,
									bbox_to_anchor=(0., 0.5),
									bbox_transform=ax.transAxes, **txt_kwargs)
				tf = ax.transData + matplotlib.transforms.Affine2D().rotate_deg(90)
				txt.set_transform(tf)
				ax.add_artist(txt)
				"""

			## Hide tick labels and axis labels
			if sharex:
				ax.tick_params(labelbottom=False, labeltop=False)
			elif xlabel_side:
				side_kwargs = {}
				if xlabel_side == 'bottom':
					side_kwargs['labeltop'] = False
					side_kwargs['labelbottom'] = True
				elif xlabel_side == 'top':
					side_kwargs['labeltop'] = True
					side_kwargs['labelbottom'] = False
				elif xlabel_side == 'both':
					side_kwargs['labeltop'] = side_kwargs['labelbottom'] = True
				elif xlabel_side == 'none':
					side_kwargs['labeltop'] = side_kwargs['labelbottom'] = False
				ax.tick_params(axis='x', **side_kwargs)
			if share_xlabel:
				ax.xaxis.label.set_visible(False)
			if ax.is_first_row():
				if xlabel_side in ('top', 'both'):
					if sharex:
						ax.tick_params(labeltop=True)
					if share_xlabel and not xlabel:
						ax.xaxis.set_label_position('top')
						ax.xaxis.label.set_visible(True)
			elif ax.is_last_row():
				if xlabel_side in ('bottom', 'both', ''):
					if sharex:
						ax.tick_params(labelbottom=True)
					if share_xlabel and not xlabel:
						ax.xaxis.set_label_position('bottom')
						ax.xaxis.label.set_visible(True)

			if sharey:
				ax.tick_params(labelleft=False, labelright=False)
			elif ylabel_side:
				side_kwargs = {}
				if ylabel_side == 'left':
					side_kwargs['labelleft'] = True
					side_kwargs['labelright'] = False
				elif ylabel_side == 'right':
					side_kwargs['labelleft'] = False
					side_kwargs['labelright'] = True
				elif ylabel_side == 'both':
					side_kwargs['labelleft'] = side_kwargs['labelright'] = True
				elif ylabel_side == 'none':
					side_kwargs['labelleft'] = side_kwargs['labelright'] = False
				ax.tick_params(axis='y', **side_kwargs)
			if share_ylabel:
				ax.yaxis.label.set_visible(False)
			if ax.is_first_col():
				if ylabel_side in ('left', 'both', ''):
					if sharey:
						ax.tick_params(labelleft=True)
					if share_ylabel and not ylabel:
						ax.yaxis.set_label_position('left')
						ax.yaxis.label.set_visible(True)
			elif ax.is_last_col():
				if ylabel_side in ('right', 'both'):
					if sharey:
						ax.tick_params(labelright=True)
					if share_ylabel and not ylabel:
						ax.yaxis.set_label_position('right')
						ax.yaxis.label.set_visible(True)

			## Axis limits
			if not (xmin is None and xmax is None):
				_xmin, _xmax = ax.get_xlim()
				xmin = _xmin if xmin is None else xmin
				xmax = _xmax if xmax is None else xmax
				ax.set_xlim(xmin, xmax)

			if not (ymin is None and ymax is None):
				_ymin, _ymax = ax.get_ylim()
				ymin = _ymin if ymin is None else ymin
				ymax = _ymax if ymax is None else ymax
				ax.set_ylim(ymin, ymax)

			if hide_axes:
				ax.set_axis_off()

	## sharex / sharey
	## Use same range for X/Y axis
	if sharex in ('all', True):
		ax0 = fig.axes[0]
		ax0.get_shared_x_axes().join(*fig.axes)
	elif sharex == 'col':
		for col in range(num_cols):
			ax0 = fig.axes[col]
			col_axes = fig.axes[col::num_cols]
			ax0.get_shared_x_axes().join(*col_axes)
	elif sharex == 'row':
		for row in range(num_rows):
			row_axes = fig.axes[(row*num_cols):(row*num_cols)+num_cols]
			ax0 = row_axes[0]
			ax0.get_shared_x_axes().join(*row_axes)

	if sharey in ('all', True):
		ax0 = fig.axes[0]
		ax0.get_shared_y_axes().join(*fig.axes)
	elif sharey == 'col':
		for col in range(num_cols):
			ax0 = fig.axes[col]
			col_axes = fig.axes[col::num_cols]
			ax0.get_shared_y_axes().join(*col_axes)
	elif sharey == 'row':
		for row in range(num_rows):
			row_axes = fig.axes[(row*num_cols):(row*num_cols)+num_cols]
			ax0 = row_axes[0]
			ax0.get_shared_y_axes().join(*row_axes)

	## Add a big axes, hide frame
	ax = fig.add_subplot(111, frameon=False)
	## hide tick and tick label of the big axes
	ax.tick_params(labelcolor='none', top='off', bottom='off',
					left='off', right='off')
	ax.grid(False)

	## Set label side
	## Note: 'both' and 'none' won't work as expected...
	if xlabel_side == 'top':
		ax.xaxis.set_label_position('top')
	else:
		ax.xaxis.set_label_position('bottom')

	if ylabel_side == 'right':
		ax.yaxis.set_label_position('right')
	else:
		ax.yaxis.set_label_position('left')

	if xlabel:
		if xlabel_side == 'top':
			xlabel += '\n'
		else:
			xlabel = '\n' + xlabel
		if isinstance(ax_label_font, (int, basestring)):
			ax.set_xlabel(xlabel, fontsize=ax_label_font)
		else:
			ax_label_font.rotation = 'horizontal'
			ax.set_xlabel(xlabel, **ax_label_font.to_kwargs())
	if ylabel:
		if ylabel_side == 'right':
			ylabel = '\n' + ylabel
		else:
			ylabel += '\n'
		if isinstance(ax_label_font, (int, basestring)):
			ax.set_ylabel(ylabel, fontsize=ax_label_font)
		else:
			ax_label_font.rotation = 'vertical'
			ax.set_ylabel(ylabel, **ax_label_font.to_kwargs())
	#if title:
	#	ax.set_title(title)

	if title:
		if isinstance(title_font, (int, basestring)):
			fig.suptitle(title, fontsize=title_font)
		else:
			title_font.rotation = 'horizontal'
			fig.suptitle(title, **title_font.to_kwargs())

	return fig
