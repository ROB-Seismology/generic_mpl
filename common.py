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


import matplotlib
import pylab


__all__ = ['show_or_save_plot']


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


def show_or_save_plot(ax_or_fig, fig_filespec=None, dpi=300, border_width=0.2):
	"""
	Show plot on screen or save it to a file

	:param ax_or_fig:
		matplotlib Axes or Figure instance
	:param fig_filespec:
		str, full path to output file
		If None, will plot on screen
		If 'wait', plotting is deferred
		(default: None)
	:param dpi:
		int, resolution of plot,
		only applies if :param:`fig_filespec` is set to output file
		(default: 300)
	:param border_width:
		float, width of border around plot frame in cm
		If None, white space will not be removed
		(default: 0.2)

	:return:
		matplotlib Axes or Figure instance if :param:`fig_filespec` is
		either None or 'wait', else None
	"""
	if isinstance(ax_or_fig, matplotlib.figure.Figure):
		fig = ax_or_fig
	else:
		fig = ax_or_fig.get_figure()

	if fig_filespec == "wait":
		return ax_or_fig
	elif fig_filespec:
		kwargs = {}
		if border_width is not None:
			kwargs = dict(bbox_inches="tight", pad_inches=border_width/2.54)
		fig.savefig(fig_filespec, dpi=dpi, **kwargs)
		pylab.clf()
	else:
		## Note, using fig.show(), the plot disappears immediately!
		#fig.show()
		pylab.show()
		return ax_or_fig
