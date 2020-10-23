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


from .common import (show_or_save_plot, common_doc)
from .frame import (plot_ax_frame, ax_frame_doc)


__all__ = ['plot_grid', 'grid_center_to_edge_coordinates',
			'grid_edge_to_center_coordinates']


def grid_center_to_edge_coordinates(Xc, Yc):
	"""
	Transform grid (or mesh) center coordinates to edge coordinates

	:param Xc:
		2D array (num_lats x num_lons), X center coordinates
	:param Yc:
		2D array (num_lats x num_lons), Y center coordinates

	:return:
		(Xe, Ye)
		2D arrays (num_lats+1 x num_lons+1), X and Y edge coordinates
	"""
	assert Xc.shape == Yc.shape

	## Output dimension
	nx, ny = Xc.shape[1] + 1, Xc.shape[0] + 1

	## First pass: compute edge coordinates along respective axes
	_Xe, _Ye = np.zeros((ny-1, nx)), np.zeros((ny, nx-1))
	dxx, dyy = np.diff(Xc, axis=1), np.diff(Yc, axis=0)
	_Xe[:,1:-1] = Xc[:,:-1] + dxx / 2.
	_Xe[:,:1] = Xc[:,:1] - dxx[:,:1] / 2.
	_Xe[:,-1:] = Xc[:,-1:] + dxx[:,-1:] / 2.
	_Ye[1:-1] = Yc[:-1] + dyy / 2.
	_Ye[:1] = Yc[:1] - dyy[:1] / 2.
	_Ye[-1:] = Yc[-1:] + dyy[-1:] / 2.

	## Second pass: compute edge coordinates along opposite axes
	Xe, Ye = np.zeros((ny, nx)), np.zeros((ny, nx))
	dxy, dyx = np.diff(_Xe, axis=0), np.diff(_Ye, axis=1)
	Xe[1:-1] = _Xe[:-1] + dxy / 2.
	Xe[:1] = _Xe[:1] - dxy[:1] / 2.
	Xe[-1:] = _Xe[-1:] + dxy[-1:] / 2.
	Ye[:,1:-1] = _Ye[:,:-1] + dyx / 2.
	Ye[:,:1] = _Ye[:,:1] + dyx[:,:1] / 2.
	Ye[:,-1:] = _Ye[:,-1:] + dyx[:,-1:] / 2.

	return (Xe, Ye)


def grid_edge_to_center_coordinates(Xe, Ye):
	"""
	Transform grid (or mesh) edge coordinates to center coordinates

	:param Xe:
		2D array (num_lats x num_lons), X edge coordinates
	:param Ye:
		2D array (num_lats x num_lons), Y edge coordinates

	:return:
		(Xc, Yc)
		2D arrays (num_lats-1 x num_lons-1), X and Y center coordinates
	"""
	## Output dimension
	nx, ny = Xe.shape[1] - 1, Xe.shape[0] - 1

	## First pass: compute center coordinates along respective axes
	_Xc, _Yc = np.zeros((ny+1, nx)), np.zeros((ny, nx+1))
	dxx, dyy = np.diff(Xe, axis=1), np.diff(Ye, axis=0)
	_Xc = Xe[:,:-1] + dxx / 2.
	_Yc = Ye[:-1] + dyy / 2.

	## Second pass: compute center coordinates along opposite axes
	dxy, dyx = np.diff(_Xc, axis=0), np.diff(_Yc, axis=1)
	Xc = _Xc[:-1] + dxy / 2.
	Yc = _Yc[:,:-1] + dyx / 2.

	return (Xc, Yc)


def plot_grid(data, X=None, Y=None,
			cmap='jet', norm=None, vmin=None, vmax=None,
			color_gradient='cont', shading=False, smoothed=False,
			colorbar=True, cax=None, cax_size=0.1, cax_padding=0.1, cax_shrink=1.,
			cbar_length=1., cbar_aspect=20, cbar_location='bottom center',
			cbar_spacing='uniform', cbar_ticks=None, cbar_label_format=None,
			cbar_label_fontsize=None, cbar_title='', cbar_title_fontsize=None,
			cbar_extend='neither', cbar_lines=False, cbar_range='full',
			contour_lines=None, contour_color='k', contour_width=0.5,
			contour_style='-', contour_labels=None, contour_label_fontsize=None,
			alpha=1,
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
			style_sheet='classic', border_width=0.2, skip_frame=False,
			fig_filespec=None, figsize=None, dpi=300, ax=None):
	"""
	Plot raster or mesh data

	:param data:
		2D array, gridded data
	:param X/Y:
		[x/ymin, x/ymax] or 1D array or 2D array or None, X/Y coodinates
		dimension may be either the same as data (= center coordinates)
		or 1 larger (= edge coordinates)
		(default: None, will just plot rectangular grid)
	:param cmap:
		str or instance of :class:`matplotlib.colors.Colormap, color palette
		(default: 'jet')
	:param norm:
		instance of :class:`matplotlib.colors.Normalize`, defining how
		to scale data values to the [0 - 1] interval, and hence to colors
		(default: None, uses default linear scaling)
	:param vmin:
	:param vmax:
		float, min/max data values to be mapped to 0/1, respectively,
		overriding vmin/vmax values of :param:`norm` if specified
		(default: None)
	:param color_gradient:
		str, if colors should be 'cont[inuous]' or 'disc[rete]'.
		Note that this mainly depends on the normalization, and can
		only be honoured in certain cases
		(default: 'cont')
	:param shading;
		bool, whether or not Gouraud shading should be applied to each
		cell or quad. Only applies if :param:`smoothed` is False
		(default: False)
	:param smoothed:
		bool, whether or not grid cells should be smoothed; this is
		accomplished using matplotlib's contourf function instead of
		pcolor(mesh)
		(default: False)
	:param colorbar:
		bool, whether or not to plot color bar
		(default: True)
	:param cax:
		matplotlib Axes instance to be used for the colorbar
		(default: None, will steal place from parent Axes instance
		given in :param:`ax`)
	:param cax_size:
		float, fraction of original Axes to use for colorbar Axes.
		Ignored if :param:`cax` is not None.
		(default: 0.10)
	:param cax_padding:
		float, fraction between colorbar and original Axes
		Ignored if :param:`cax` is not None.
		(default: 0.10)
	:param cax_shrink:
		float, fraction by which to shrink cax
		Ignored if :param:`cax` is not None.
		(default: 1.)
	:param cbar_length:
		float, length of colorbar as fraction of Axes width or height
		Ignored if :param:`cax` is not None.
		(default: 1.)
	:param cbar_aspect:
		float, aspect ratio (long/short dimension) of colorbar
		Ignored if :param:`cax` is not None.
		(default: 20)
	:param cbar_location:
		str, location (side of parent axes) and alignment of colorbar,
		location: 'left' / 'right' (vertical), 'top' / 'bottom' (horizontal)
		alignment: 'center' or 'left' / 'right' (if orientation is horizontal)
		or 'top' / 'bottom' (if orientation is vertical)
		Ignored if :param:`cax` is not None.
		(default: 'bottom center')
	:param cbar_spacing:
		str, either 'uniform' (each discrete color gets the same space)
		or 'proportional' (space proportional to represented data interval)
		(default: 'uniform')
	:param cbar_ticks:
		list or array, tick positions for colorbar
		(default: None, will position ticks automatically)
	:param cbar_label_format:
		str or instance of :class:`matplotlib.ticker.Formatter`, format for
		colorbar tick labels (e.g., '%.2f')
		(default: None)
	:param cbar_label_fontsize:
		int or str, font size to use for axis tick labels
		(default: None, will use value of :param:`tick_label_fontsize`)
	:param cbar_title:
		str, title for colorbar
		(default: '')
	:param cbar_title_fontsize:
		int or str, font size to use for axis tick labels
		(default: None, will use value of :param:`ax_label_fontsize`)
	:param cbar_extend:
		str, if and how colorbar should be extended with triangular
		ends for out-of-range values, one of 'neither', 'both',
		'min' or 'max'
		(default: 'neither')
	:param cbar_lines:
		bool, whether or not lines should be drawn at color boundaries
		in colorbar
		(default: False)
	:param cbar_range:
		str, colorbar range, indicating if colorbar should show full
		range in colormap ('full') or only the data range ('data')
		(default: 'full')
	:param contour_lines:
		int, list or array, values of contour lines to be drawn on top of grid:
		- 'None' or 0 = no contours
		- N (int): number of contours
		- list or array specifying contour values
		(default: None)
	:param contour_color:
		matplotlib color specification (or list), color to use for contour
		lines (default: 'k')
	:param contour_width:
		float or list, line width(s) of contour lines
		(default: 0.5)
	:param contour_style:
		str or list, line style(s) of contour lines: '-', '--', ':' or '-:'
		(default: '-')
	:param contour_labels:
		list, labels for contour lines. If None, use the contour
		line values; if empty list, no labels will be drawn
		(default: None)
	:param contour_label_fontsize:
		int or str, font size to use for axis tick labels
		(default: None, will use value of :param:`cbar_label_fontsize`)
	:param alpha:
		float in the range 0 - 1, grid opacity
		(default: 1)
	"""
	frame_args = {key: val for (key, val) in locals().items()
				if not key in ['data', 'X', 'Y', 'cmap', 'norm', 'vmin', 'vmax',
							'color_gradient', 'shading', 'smoothed',
							'colorbar', 'cax', 'cax_size', 'cax_padding',
							'cax_shrink', 'cbar_length', 'cbar_aspect',
							'cbar_location', 'cbar_spacing', 'cbar_ticks',
							'cbar_label_format', 'cbar_label_fontsize',
							'cbar_title', 'cbar_title_fontsize',
							'cbar_extend', 'cbar_lines', 'cbar_range',
							'contour_lines', 'contour_color', 'contour_width',
							'contour_style', 'contour_labels',
							'contour_label_fontsize', 'alpha', 'style_sheet',
							'border_width', 'skip_frame', 'fig_filespec',
							'figsize', 'dpi', 'ax', 'kwargs']}

	from mpl_toolkits.axes_grid1.inset_locator import inset_axes
	from matplotlib.colors import BoundaryNorm
	from matplotlib.colorbar import make_axes, ColorbarBase
	from mapping.layeredbasemap.cm.norm import (PiecewiseLinearNorm,
												PiecewiseConstantNorm)

	pylab.style.use(style_sheet)

	if cbar_title_fontsize is None:
		cbar_title_fontsize = ax_label_fontsize
	if cbar_label_fontsize is None:
		cbar_label_fontsize = tick_label_fontsize
	if contour_label_fontsize is None:
		contour_label_fontsize = cbar_label_fontsize

	if ax is None:
		if fig_filespec:
			pylab.ioff()
		fig, ax = pylab.subplots(figsize=figsize, facecolor='white')
	else:
		fig = ax.get_figure()

	## Determine if we need center or edge coordinates or both
	need_center_coordinates = False
	need_edge_coordinates = False
	if smoothed or shading or contour_lines is not None or contour_lines != 0:
		need_center_coordinates = True
	if not smoothed:
		need_edge_coordinates = True

	## Construct X/Y arrays
	if X is not None and Y is not None:
		if len(X) == len(Y) == 2:
			## X/Y specified as x/ymin / x/ymax
			nx, ny = data.shape[1], data.shape[0]
			if need_edge_coordinates:
				nx, ny = nx + 1, ny + 1
			X = np.linspace(X[0], X[1], nx)
			Y = np.linspace(Y[0], Y[1], ny)
		if len(X.shape) == len(Y.shape) == 1:
			## X/Y are 1D arrays
			X, Y = np.meshgrid(X, Y)

		if X.shape == data.shape:
			## Center coordinates
			Xc, Yc = X, Y
			if need_edge_coordinates:
				print("Transforming center to edge coordinates!")
				Xe, Ye = grid_center_to_edge_coordinates(Xc, Yc)
			else:
				Xe, Ye = None, None
		elif X.shape[0] == data.shape[0] + 1:
			## Edge coordinates
			Xe, Ye = X, Y
			if need_center_coordinates:
				print("Transforming edge to center coordinates!")
				Xc, Yc = grid_edge_to_center_coordinates(Xe, Ye)
			else:
				Xc, Yc = None, None
		else:
			raise Exception('Dimensions of data and coordinates do not match!')

	## Mask NaN values
	if not isinstance(data, np.ma.MaskedArray):
		data = np.ma.masked_array(data, mask=np.isnan(data))

	if isinstance(cmap, basestring):
		cmap = matplotlib.cm.get_cmap(cmap)

	## Try to convert to piecewise constant norm or limit the number of colors
	## in the color palette if color_gradient is 'discontinuous'
	if color_gradient[:4] == 'disc':
		if norm is None:
			if vmin is None:
				vmin = np.nanmin(data)
			if vmax is None:
				vmax = np.nanmax(data)
			norm = BoundaryNorm(np.linspace(vmin, vmax, 8), cmap.N)
		if isinstance(norm, PiecewiseLinearNorm):
			norm = norm.to_piecewise_constant_norm()
		elif not isinstance(norm, (PiecewiseConstantNorm, BoundaryNorm)):
			print('Warning: need constant norm to plot discrete colors')
			## Alternatively, we can try limiting the number of colors in the palette
			if not isinstance(cmap, matplotlib.colors.Colormap):
				cmap = matplotlib.cm.get_cmap(cmap, 10)

	## Plot grid
	cs = None
	common_kwargs = {'cmap': cmap, 'norm': norm, 'vmin': vmin, 'vmax': vmax,
					'alpha': alpha}

	if smoothed:
		## data must have same size as X and Y for contourf
		if color_gradient[:4] == 'disc':
			V = getattr(norm, 'breakpoints', getattr(norm, 'boundaries'))
			if X is None and Y is None:
				cs = ax.contourf(data, V, **common_kwargs)
			else:
				cs = ax.contourf(Xc, Yc, data, V, **common_kwargs)
		else:
			#V = 1100
			V = cmap.N
			if X is None and Y is None:
				cs = ax.contourf(data, V, **common_kwargs)
			else:
				cs = ax.contourf(Xc, Yc, data, V, **common_kwargs)

	else:
		## both pcolor and pcolormesh need edge coordinates,
		## except if shading == 'gouraud'
		if X is None and Y is None:
			shading = {True: 'gouraud', False: 'flat'}[shading]
			cs = ax.pcolormesh(data, shading=shading, **common_kwargs)
			# or use imshow, which has interpolation possibilities?

		else:
			if shading:
				cs = ax.pcolormesh(Xc, Yc, data, shading='gouraud', **common_kwargs)
			else:
				cs = ax.pcolormesh(Xe, Ye, data, shading='flat', **common_kwargs)

	## Contour lines
	if contour_lines is not None:
		# X and Y must have same shape as data !
		cl = ax.contour(Xc, Yc, data, contour_lines, colors=contour_color,
					linewidths=contour_width, linestyles=contour_style)

		## Contour labels:
		if contour_labels is None:
			contour_labels = contour_lines
		if contour_labels is not None:
			clabels = ax.clabel(cl, contour_labels, colors=contour_color, inline=True,
								fontsize=contour_label_fontsize, fmt=cbar_label_format)
		# TODO: white background for contour labels
		#bbox_args = label_style.to_kwargs()['bbox']
		#[txt.set_bbox(bbox_args) for txt in clabels]

	## Frame
	if not skip_frame:
		plot_ax_frame(ax, x_is_date=False, y_is_date=False, **frame_args)

	## Color bar
	if colorbar:
		cbar_align = 'center'
		if ' ' in cbar_location:
			cbar_location, cbar_align = cbar_location.split()

		if cbar_location in ("top", "bottom"):
			cbar_orientation = "horizontal"
		else:
			cbar_orientation = "vertical"

		if cax is None:
			#ax_pos = ax.get_position()
			#fig = ax.get_figure()
			#cax = fig.add_axes([ax_pos.x1+0.01, ax_pos.y0, 0.02, ax_pos.height])

			#from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
			#divider = make_axes_locatable(ax)
			#if cbar_orientation == 'vertical':
			#	size = axes_size.AxesY(ax, aspect=1./cbar_aspect)
			#else:
			#	size = axes_size.AxesX(ax, aspect=1./cbar_aspect)
			#pad = axes_size.Fraction(cbar_padding, size)
			#cax = divider.append_axes(cbar_location, size=size, pad=pad)

			cbar_aspect *= cbar_length
			cax, _ = make_axes(ax, location=cbar_location, fraction=cax_size,
							aspect=cbar_aspect, shrink=cax_shrink, pad=cax_padding)

			## Necessary for ax.get_position to return correct size
			ax.apply_aspect()
			ax_pos = ax.get_position(original=False)

			cax_pos = cax.get_position()
			left, bottom = cax_pos.x0, cax_pos.y0
			width, height = cax_pos.width, cax_pos.height
			if cbar_orientation == 'vertical':
				bottom, height = ax_pos.y0, ax_pos.height
				unshrinked_height = height / cax_shrink
				center = bottom + height / 2
				height *= cbar_length
				if cbar_align == 'center':
					bottom = center - height / 2
				elif cbar_align == 'top':
					top = center + unshrinked_height / 2
					bottom = top - height
				elif cbar_align == 'bottom':
					bottom = center - unshrinked_height / 2
			elif cbar_orientation == 'horizontal':
				left, width = ax_pos.x0, ax_pos.width
				unshrinked_width = width / cax_shrink
				center = left + width / 2
				width *= cbar_length
				if cbar_align == 'center':
					left = center - width / 2
				elif cbar_align == 'right':
					right = center + unshrinked_width / 2
					left = right - width
				elif cbar_align == 'left':
					left = center - unshrinked_width / 2
			cax.set_position((left, bottom, width, height))

		elif isinstance(cax, tuple):
			## Test
			anchor = cax
			cax = None

		elif cax == 'inside':
			if cbar_orientation == 'horizontal':
				width = cbar_length
				height = width / cbar_aspect
				loc = cbar_location + ' ' + cbar_align
			else:
				height = cbar_length
				width = height / cbar_aspect
				loc = cbar_align + ' ' + cbar_location
			width = '%.0f%%' % (width * 100)
			height = '%.0f%%' % (height * 100)
			loc = loc.replace('top', 'upper').replace('bottom', 'lower')
			loc = {'upper right': 1,
					'upper left': 2,
					'lower left': 3,
					'lower right': 4,
					'right': 5,
					'center left': 6,
					'center right': 7,
					'lower center': 8,
					'upper center': 9,
					'center': 10}[loc]
			cax = inset_axes(ax, width=width, height=height, loc=loc,
							borderpad=cax_padding)

		if cax:
			sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
			sm.set_array(data)
			if color_gradient == 'disc':
				boundaries = getattr(norm, 'breakpoints', getattr(norm, 'boundaries'))
				if cbar_extend in ('left', 'both'):
					boundaries = np.hstack([[-1E+12], boundaries])
				if cbar_extend in ('right', 'both'):
					boundaries = np.hstack([boundaries, [1E+12]])
				if cbar_range == 'data':
					start = np.where(boundaries < np.nanmin(data))[0][-1]
					end = np.where(boundaries > np.nanmax(data))[0][0]
					boundaries = boundaries[start:end+1]
			else:
				boundaries = None
				if cbar_range == 'data':
					sm.set_clim(vmin=np.nanmin(data), vmax=np.nanmax(data))

			cbar = pylab.colorbar(sm, cax=cax, orientation=cbar_orientation,
							spacing=cbar_spacing, ticks=cbar_ticks,
							format=cbar_label_format, extend=cbar_extend,
							drawedges=cbar_lines, boundaries=boundaries)
			#elif cbar_range == 'full':
			#	cbar = ColorbarBase(cax, cmap=cmap, norm=norm,
			#				boundaries=boundaries, orientation=cbar_orientation,
			#				spacing=cbar_spacing, ticks=cbar_ticks,
			#				format=cbar_label_format, extend=cbar_extend,
			#				drawedges=cbar_lines)

		if cbar_orientation == 'horizontal':
			cbar.set_label(cbar_title, size=cbar_title_fontsize)
		else:
			cbar.ax.set_title(cbar_title, size=cbar_title_fontsize)
		cbar.ax.tick_params(labelsize=cbar_label_fontsize)

		# TODO: boundaries / values, cf. layeredbasemap ?


	## Output
	return show_or_save_plot(ax, fig_filespec=fig_filespec, dpi=dpi,
							border_width=border_width)

plot_grid.__doc__ += (ax_frame_doc + common_doc)
