"""
Generic plot functions based on matplotlib
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import int

try:
	## Python 2
	basestring
except:
	## Python 3
	basestring = str


import pylab
import matplotlib
import matplotlib.ticker
import matplotlib.dates as mpl_dates


__all__ = ['plot_ax_frame']


MPL_FONT_SIZES = ['xx-small', 'x-small', 'small', 'medium',
				'large', 'x-large', 'xx-large']

MPL_INTERVAL_DICT = {'Y': 0, 'M': 1, 'W': 2, 'D': 3, 'h': 4, 'm': 5, 's': 6}

MPL_DATE_LOCATOR_DICT = {'Y': mpl_dates.YearLocator,
						'M': mpl_dates.MonthLocator,
						'd': mpl_dates.WeekdayLocator,
						'D': mpl_dates.DayLocator,
						'h': mpl_dates.HourLocator,
						'm': mpl_dates.MinuteLocator,
						's': mpl_dates.SecondLocator}


def _create_date_locator(tick_interval):
	"""
	Create matplotlib date locator from tick interval specification

	:param tick_interval:
		- 0 (= no ticks)
		- None (= automatic ticks)
		- string XXY, with XX interval and Y time unit:
			'Y', 'M', 'D', 'd', 'h', 'm', 's'
			(year|month|day|weekday|hour|minute|second)

	:return:
		matplotlib date locator object
	"""
	if tick_interval == 0:
			date_loc = matplotlib.ticker.NullLocator()
	elif tick_interval is None:
		date_loc = mpl_dates.AutoDateLocator(interval_multiples=True)
	else:
		if isinstance(tick_interval, basestring):
			val, tick_unit = int(tick_interval[:-1]), tick_interval[-1:]
		else:
			val = tick_interval
			tick_unit = 'Y'
		#tu_key = MPL_INTERVAL_DICT[tick_unit]
		#for key in range(tu_key):
		#	date_loc.intervald[key] = []
		#date_loc.intervald[tu_key] = [val]
		loc_kwargs = {}
		loc_kwargs[{'Y': 'base'}.get(tick_unit, 'interval')] = val
		date_loc = MPL_DATE_LOCATOR_DICT[tick_unit](**loc_kwargs)

	return date_loc


ax_frame_doc = """

	Frame arguments:

	:param xscaling:
		str, scaling to use for X axis ('lin' or 'log')
		Prepend '-' to invert orientation of X axis
		(default: 'lin')
	:param yscaling:
		str, scaling to use for Y axis ('lin' or 'log')
		Prepend '-' to invert orientation of Y axis
		(default: 'lin')
	:param xmin:
		float, start value for X axis
		Note that, if X values of :param:`datasets` are datetimes,
		this should be datetime also
		(default: None, let matplotlib decide)
	:param xmax:
		float, end value for X axis
		Note that, if X values of :param:`datasets` are datetimes,
		this should be datetime also
		(default: None, let matplotlib decide)
	:param ymin:
		float, start value for Y axis
		Note that, if Y values of :param:`datasets` are datetimes,
		this should be datetime also
		(default: None, let matplotlib decide)
	:param ymax:
		float, end value for Y axis
		Note that, if Y values of :param:`datasets` are datetimes,
		this should be datetime also
		(default: None, let matplotlib decide)
	:param xlabel:
		str, label for X axis
		(default: '')
	:param ylabel:
		str, label for Y axis
		(default: '')
	:param ax_label_fontsize:
		int or str, font size to use for axis labels
		(default: 'large')
	:param xticks:
		list or array, X axis tick positions
		Note that, if X values of :param:`datasets` are datetimes,
		these should be datetimes also
		(default: None, let matplotlib decide)
	:param xticklabels:
		X axis tick labels, either:
		- None (= automatic labels)
		- list of labels corresponding to :param:`xticks`
		- matplotlib Formatter object
		- format string (for dates or scalars)
		- '' or [] (= no tick labels)
		(default: None, let matplotlib decide)
	:param xtick_interval:
		X axis tick interval specification
		single value (major ticks only) or tuple (major/minor ticks) of:
		- matplotlib Locator object
		- None (= automatic ticks)
		- 0 (= no ticks)
		- int (= integer tick interval)
		- str (= tick interval for dates, where last char is in YMDdhms
			(year|month|day|weekday|hour|minute|second)
		(default: None)
	:param xtick_rotation:
		float, rotation angle for X axis tick labels
		(default: 0)
	:param xtick_direction:
		str, X axis tick direction: 'in', 'out' or 'both'
		(default: '')
	:param xtick_side:
		str, on which side of the plot X ticks should be drawn:
		'bottom', 'top' or 'both'
		(default: '')
	:param yticks:
		list or array, Y axis tick positions
		Note that, if Y values of :param:`datasets` are datetimes,
		these should be datetimes also
		(default: None, let matplotlib decide)
	:param yticklabels:
		Y axis tick labels
		See :param:`xticklabels` for options
	:param ytick_interval:
		Y axis tick interval specification
		see :param:`xtick_interval` for options
	:param ytick_rotation:
		float, rotation angle for Y axis tick labels
		(default: 0)
	:param ytick_direction:
		str, Y axis tick direction: 'in', 'out' or 'both'
		(default: '')
	:param ytick_side:
		str, on which side of the plot Y ticks should be drawn:
		'left', 'right' or 'both'
		(default: '')
	:param tick_label_fontsize:
		int or str, font size to use for axis tick labels
		(default: 'medium')
	:param tick_params:
		dict, containing keyword arguments for :func:`ax.tick_params`,
		that will be applied to both the X and Y axes
		(default: {})
	:param title:
		str, plot title
		(default: '')
	:param title_fontsize:
		str, font size to use for plot title
		(default: 'large')
	:param xgrid:
		int, 0/1/2/3 = draw no/major/minor/major+minor X grid lines
		(default: 0)
	:param ygrid:
		int, 0/1/2/3 = draw no/major/minor/major+minor Y grid lines
		(default: 0)
	:param aspect_ratio:
		float, vertical-to-horizontal aspect ratio in data units
		or str ('equal', 'auto')
		(default: None)
	:param hlines:
		[y, xmin, xmax] list of arrays (of same length) or scalars
		If xmin or xmax are None, limits of X axis will be used
		(default: [])
	:param hline_args:
		dict, containing keyword arguments understood by :func:`pylab.hlines`
		(e.g., 'colors', 'linestyles', 'linewidth', 'label')
		(default: {})
	:param vlines:
		[x, ymin, ymax] list of arrays (of same length) or scalars
		If ymin or ymax are None, limints of Y axis will be used
		(default: [])
	:param vline_args:
		dict, containing keyword arguments understood by :func:`pylab.vlines`
		(e.g., 'colors', 'linestyles', 'linewidth', 'label')
		(default: {})
"""


common_doc = """

	:param legend_location:
		int or str, location of legend (matplotlib location code):
			"best" 	0
			"upper right" 	1
			"upper left" 	2
			"lower left" 	3
			"lower right" 	4
			"right" 		5
			"center left" 	6
			"center right" 	7
			"lower center" 	8
			"upper center" 	9
			"center" 		10
		(default: 0)
	:param legend_fontsize:
		int or str, font size to use for legend labels
		If not specified, will use the value of :param:`tick_label_fontsize`
		(default: 'medium')
	:param style_sheet:
		str, matplotlib style sheet to apply to plot
		See matplotlib.style.available for availabel style sheets
		(default: 'classic')
	:param border_width:
		float, width of border around plot frame in cm
		If None, white space will not be removed
		(default: 0.2)
	:param skip_frame:
		bool, whether or not to skip plotting the axes frame
		(default: False)
	:param fig_filespec:
		str, full path to output file
		If None, will plot on screen
		If 'wait', plotting is deferred
		(default: None)
	:param figsize:
		(width, height) tuple of floats, plot size in inches,
		only applies if :param:`ax` is None
		(default: None)
	:param dpi:
		int, resolution of plot,
		only applies if :param:`fig_filespec` is set to output file
		(default: 300)
	:param ax:
		matplotlib Axes instance, in which plot will be drawn
		If specified, :param:`fig_filespec` will be overridden with 'wait'
		(default: None, will generate new Axes instance)

	:return:
		matplotlib Axes instance if :param:`fig_filespec` is either None
		or 'wait', else None
"""


def plot_ax_frame(ax, x_is_date=False, y_is_date=False,
				xscaling='lin', yscaling='lin',
				xmin=None, xmax=None, ymin=None, ymax=None,
				xlabel='', ylabel='', ax_label_fontsize='large',
				xticks=None, xticklabels=None, xtick_interval=None, xtick_rotation=0,
				xtick_direction='', xtick_side='',
				yticks=None, yticklabels=None, ytick_interval=None, ytick_rotation=0,
				ytick_direction='', ytick_side='',
				tick_label_fontsize='medium', tick_params={},
				title='', title_fontsize='large',
				xgrid=0, ygrid=0, aspect_ratio=None,
				hlines=[], hline_args={}, vlines=[], vline_args={}):
	"""
	Plot ax frame

	:param ax:
		matplotlib Axes instance, in which frame will be drawn
	:param x_is_date:
		bool, whether or not X axis contains datetimes
		(default: False)
	:para y_is_date:
		bool, whether or not Y axis contains datetimes
		(default: False)

	:return:
		None
	"""
	## Axis limits
	_xmin, _xmax = ax.get_xlim()
	xmin = _xmin if xmin is None else xmin
	xmax = _xmax if xmax is None else xmax
	ax.set_xlim(xmin, xmax)

	_ymin, _ymax = ax.get_ylim()
	ymin = _ymin if ymin is None else ymin
	ymax = _ymax if ymax is None else ymax
	ax.set_ylim(ymin, ymax)

	## Axis scaling
	if xscaling[0] == '-':
		xscaling = xscaling[1:]
		ax.invert_xaxis()
	xscaling = {'lin': 'linear', 'log': 'log'}[xscaling[:3]]
	ax.set_xscale(xscaling)
	if yscaling[0] == '-':
		yscaling = yscaling[1:]
		ax.invert_yaxis()
	yscaling = {'lin': 'linear', 'log': 'log'}[yscaling[:3]]
	ax.set_yscale(yscaling)

	## Vertical / horizontal aspect ratio (in data units)
	if aspect_ratio is not None:
		ax.set_aspect(aspect_ratio)

	## Axis labels
	if xlabel:
		ax.set_xlabel(xlabel, fontsize=ax_label_fontsize)
	if ylabel:
		ax.set_ylabel(ylabel, fontsize=ax_label_fontsize)

	## Horizontal / vertical lines
	if hlines:
		y, xmin, xmax = hlines
		_xmin, _xmax = ax.get_xlim()
		xmin = _xmin if xmin is None else xmin
		xmax = _xmax if xmax is None else xmax
		ax.hlines(y, xmin, xmax, **hline_args)

	if vlines:
		x, ymin, ymax = vlines
		_ymin, _ymax = ax.get_ylim()
		ymin = _ymin if ymin is None else ymin
		ymax = _ymax if ymax is None else ymax
		ax.vlines(x, ymin, ymax, **vline_args)

	## X ticks
	if xticks is not None:
		ax.set_xticks(xticks)
	#elif xtick_interval is not None:
	else:
		if isinstance(xtick_interval, tuple) and len(xtick_interval) == 2:
			major_tick_interval, minor_tick_interval = xtick_interval
		else:
			major_tick_interval, minor_tick_interval = xtick_interval, None

		if isinstance(major_tick_interval, matplotlib.ticker.Locator):
			major_loc = major_tick_interval
		elif x_is_date:
			major_loc = _create_date_locator(major_tick_interval)
		elif major_tick_interval:
			major_loc = matplotlib.ticker.MultipleLocator(major_tick_interval)
		elif major_tick_interval is None:
			if xscaling[:3] == 'log':
				major_loc = matplotlib.ticker.LogLocator()
			else:
				major_loc = matplotlib.ticker.AutoLocator()
		else:
			major_loc = matplotlib.ticker.NullLocator()
		ax.xaxis.set_major_locator(major_loc)
		if isinstance(major_loc, mpl_dates.DateLocator):
			if xticklabels is None:
				ax.xaxis.set_major_formatter(mpl_dates.AutoDateFormatter(locator=major_loc))

		if isinstance(minor_tick_interval, matplotlib.ticker.Locator):
			minor_loc = minor_tick_interval
		elif x_is_date:
			minor_loc = _create_date_locator(minor_tick_interval)
		elif minor_tick_interval:
			minor_loc = matplotlib.ticker.MultipleLocator(minor_tick_interval)
		elif minor_tick_interval is None:
			minor_loc = matplotlib.ticker.AutoLocator()
		else:
			minor_loc = matplotlib.ticker.NullLocator()
		ax.xaxis.set_minor_locator(minor_loc)
		## Note: no formatter for minor ticks, as we don't print them

	## X ticklabels
	if xscaling[:3] == 'log' and xticklabels is None:
		## Do not use log notation for small exponents
		if xmin > 1E-4 and xmax < 1E+4:
			xticklabels = matplotlib.ticker.FormatStrFormatter('%g')
	if isinstance(xticklabels, matplotlib.ticker.Formatter):
		ax.xaxis.set_major_formatter(xticklabels)
	elif isinstance(xticklabels, basestring):
		if xticklabels == '':
			major_formatter = matplotlib.ticker.NullFormatter()
		elif x_is_date:
			major_formatter = mpl_dates.DateFormatter(xticklabels)
		else:
			major_formatter = matplotlib.ticker.FormatStrFormatter(xticklabels)
		ax.xaxis.set_major_formatter(major_formatter)
	elif xticklabels is not None:
		ax.set_xticklabels(xticklabels)

	## Y ticks
	if yticks is not None:
		ax.set_yticks(yticks)
	#if ytick_interval is not None:
	else:
		if isinstance(ytick_interval, tuple) and len(ytick_interval) == 2:
			major_tick_interval, minor_tick_interval = ytick_interval
		else:
			major_tick_interval, minor_tick_interval = ytick_interval, None

		if isinstance(major_tick_interval, matplotlib.ticker.Locator):
			major_loc = major_tick_interval
		elif y_is_date:
			major_loc = _create_date_locator(major_tick_interval)
		elif major_tick_interval:
			major_loc = matplotlib.ticker.MultipleLocator(major_tick_interval)
		elif major_tick_interval is None:
			if yscaling[:3] == 'log':
				major_loc = matplotlib.ticker.LogLocator()
			else:
				major_loc = matplotlib.ticker.AutoLocator()
		else:
			major_loc = matplotlib.ticker.NullLocator()
		ax.yaxis.set_major_locator(major_loc)
		if isinstance(major_loc, mpl_dates.DateLocator):
			if yticklabels is None:
				ax.yaxis.set_major_formatter(mpl_dates.AutoDateFormatter(locator=major_loc))

		if isinstance(minor_tick_interval, matplotlib.ticker.Locator):
			minor_loc = minor_tick_interval
		elif y_is_date:
			minor_loc = _create_date_locator(minor_tick_interval)
		elif minor_tick_interval:
			minor_loc = matplotlib.ticker.MultipleLocator(minor_tick_interval)
		elif minor_tick_interval is None:
			minor_loc = matplotlib.ticker.AutoMinorLocator()
		else:
			minor_loc = matplotlib.ticker.NullLocator()
		ax.yaxis.set_minor_locator(minor_loc)
		## Note: no formatter for minor ticks, as we don't print them

	## Y tick labels
	if yscaling[:3] == 'log' and yticklabels is None:
		## Do not use log notation for small exponents
		if ymin > 1E-4 and ymax < 1E+4:
			yticklabels = matplotlib.ticker.FormatStrFormatter('%g')
	if isinstance(yticklabels, matplotlib.ticker.Formatter):
		ax.yaxis.set_major_formatter(yticklabels)
	elif isinstance(yticklabels, basestring):
		if yticklabels == '':
			major_formatter = matplotlib.ticker.NullFormatter()
		elif y_is_date:
			major_formatter = mpl_dates.DateFormatter(yticklabels)
		else:
			major_formatter = matplotlib.ticker.FormatStrFormatter(yticklabels)
		ax.yaxis.set_major_formatter(major_formatter)
	elif yticklabels is not None:
		ax.set_yticklabels(yticklabels)

	## Tick label size and rotation
	for label in ax.get_xticklabels() + ax.get_yticklabels():
		label.set_size(tick_label_fontsize)

	if xtick_rotation:
		for label in ax.get_xticklabels():
			label.set_horizontalalignment('right')
			label.set_rotation(xtick_rotation)

	if ytick_rotation:
		for label in ax.get_yticklabels():
			label.set_horizontalalignment('right')
			label.set_rotation(ytick_rotation)

	## Tick aspect
	if tick_params:
		ax.tick_params(axis='both', **tick_params)

	if xtick_direction:
		ax.tick_params(axis='x', direction=xtick_direction)

	if xtick_side:
		side_kwargs = {}
		if xtick_side in ('top', 'both'):
			side_kwargs['top'] = True
		if xtick_side in ('bottom', 'both'):
			side_kwargs['bottom'] = True
		ax.tick_params(axis='x', **side_kwargs)

	if ytick_direction:
		ax.tick_params(axis='y', direction=ytick_direction)

	if ytick_side:
		side_kwargs = {}
		if ytick_side in ('left', 'both'):
			side_kwargs['left'] = True
		if ytick_side in ('right', 'both'):
			side_kwargs['right'] = True
		ax.tick_params(axis='y', **side_kwargs)

	## Grid
	if xgrid:
		which = {1: 'major', 2: 'minor', 3: 'both'}[xgrid]
		ax.grid(True, which=which, axis='x')
	if ygrid:
		which = {1: 'major', 2: 'minor', 3: 'both'}[ygrid]
		ax.grid(True, which=which, axis='y')

	## Title
	if title:
		ax.set_title(title, fontsize=title_fontsize)

plot_ax_frame.__doc__ += ax_frame_doc
