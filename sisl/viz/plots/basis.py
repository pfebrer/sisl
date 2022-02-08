import sisl
from .grid import GridPlot
from ..plot import entry_point
from ..input_fields import SislObjectInput, FloatInput, OrbitalQueries, TextInput, ColorInput, FloatInput

import numpy as np

class BasisPlot(GridPlot):
    """Representation of the basis orbitals

    Parameters
    ----------
    geometry: Geometry, optional
    	Geometry to take the basis orbitals from.
    grid_prec: float, optional
    	The spacing between points of the grid where the basis will be
    	projected (in Ang).             If you are plotting a 3D
    	representation, take into account that a very fine and big grid could
    	result in             your computer crashing on render. If it's the
    	first time you are using this function,             assess the
    	capabilities of your computer by first using a low-precision grid and
    	increase             it gradually.
    orbitals: array-like of dict, optional
    	Multiple queries to select the basis orbitals to be plotted.   Each
    	item is a dict.    Structure of the dict: {         'name':
    	'species':          'atoms':    Structure of the dict: {
    	'index':    Structure of the dict: {         'in':  }         'fx':
    	'fy':          'fz':          'x':          'y':          'z':
    	'Z':          'neighbours':    Structure of the dict: {
    	'range':          'R':          'neigh_tag':  }         'tag':
    	'seq':  }         'orbitals':          'color':          'neg_color':
    	'opacity':  }
    grid: Grid, optional
    	A sisl.Grid object. If provided, grid_file is ignored.
    grid_file: cubeSile or rhoSileSiesta or ldosSileSiesta or rhoinitSileSiesta or rhoxcSileSiesta or drhoSileSiesta or baderSileSiesta or iorhoSileSiesta or totalrhoSileSiesta or stsSileSiesta or stmldosSileSiesta or hartreeSileSiesta or neutralatomhartreeSileSiesta or totalhartreeSileSiesta or gridncSileSiesta or ncSileSiesta or fdfSileSiesta or tsvncSileSiesta or chgSileVASP or locpotSileVASP, optional
    	A filename that can be return a Grid through `read_grid`.
    represent:  optional
    	The representation of the grid that should be displayed
    transforms:  optional
    	Transformations to apply to the whole grid.             It can be a
    	function, or a string that represents the path             to a
    	function (e.g. "scipy.exp"). If a string that is a single
    	word is provided, numpy will be assumed to be the module (e.g.
    	"square" will be converted into "np.square").              Note that
    	transformations will be applied in the order provided. Some
    	transforms might not be necessarily commutable (e.g. "abs" and
    	"cos").
    axes:  optional
    	The axis along you want to see the grid, it will be reduced along the
    	other ones, according to the the `reduce_method` setting.
    zsmooth:  optional
    	Parameter that smoothens how data looks in a heatmap.
    	'best' interpolates data, 'fast' interpolates pixels, 'False'
    	displays the data as is.
    interp: array-like, optional
    	Interpolation factors to make the grid finer on each axis.See the
    	zsmooth setting for faster smoothing of 2D heatmap.
    transform_bc:  optional
    	The boundary conditions when a cell transform is applied to the grid.
    	Cell transforms are only             applied when the grid's cell
    	doesn't follow the cartesian coordinates and the requested display is
    	2D or 1D.
    nsc: array-like, optional
    	Number of times the grid should be repeated
    offset: array-like, optional
    	The offset of the grid along each axis. This is important if you are
    	planning to match this grid with other geometry related plots.
    trace_name: str, optional
    	The name that the trace will show in the legend. Good when merging
    	with other plots to be able to toggle the trace in the legend
    x_range: array-like of shape (2,), optional
    	Range where the X is displayed. Should be inside the unit cell,
    	otherwise it will fail.
    y_range: array-like of shape (2,), optional
    	Range where the Y is displayed. Should be inside the unit cell,
    	otherwise it will fail.
    z_range: array-like of shape (2,), optional
    	Range where the Z is displayed. Should be inside the unit cell,
    	otherwise it will fail.
    crange: array-like of shape (2,), optional
    	The range of values that the colorbar must enclose. This controls
    	saturation and hides below threshold values.
    cmid: int, optional
    	The value to set at the center of the colorbar. If not provided, the
    	color range is used
    colorscale: str, optional
    	A valid plotly colorscale. See https://plotly.com/python/colorscales/
    reduce_method:  optional
    	The method used to reduce the dimensions that will not be displayed
    	in the plot.
    isos: array-like of dict, optional
    	The isovalues that you want to represent.             The way they
    	will be represented is of course dependant on the type of
    	representation:                 - 2D representations: A contour (i.e.
    	a line)                 - 3D representations: A surface
    	Each item is a dict.    Structure of the dict: {         'name': The
    	name of the iso query. Note that you can use $isoval$ as a template
    	to indicate where the isoval should go.         'val': The iso value.
    	If not provided, it will be infered from `frac`         'frac': If
    	val is not provided, this is used to calculate where the isosurface
    	should be drawn.                     It calculates them from the
    	minimum and maximum values of the grid like so:
    	If iso_frac = 0.3:                     (min_value-----
    	ISOVALUE(30%)-----------max_value)                     Therefore, it
    	should be a number between 0 and 1.
    	'step_size': The step size to use to calculate the isosurface in case
    	it's a 3D representation                     A bigger step-size can
    	speed up the process dramatically, specially the rendering part
    	and the resolution may still be more than satisfactory (try to use
    	step_size=2). For very big                     grids your computer
    	may not even be able to render very fine surfaces, so it's worth
    	keeping                     this setting in mind.         'color':
    	The color of the surface/contour.         'opacity': Opacity of the
    	surface/contour. Between 0 (transparent) and 1 (opaque). }
    plot_geom: bool, optional
    	If True the geometry associated to the grid will also be plotted
    geom_kwargs: dict, optional
    	Extra arguments that are passed to geom.plot() if plot_geom is set to
    	True
    root_fdf: fdfSileSiesta, optional
    	Path to the fdf file that is the 'parent' of the results.
    results_path: str, optional
    	Directory where the files with the simulations results are
    	located. This path has to be relative to the root fdf.
    entry_points_order: array-like, optional
    	Order with which entry points will be attempted.
    backend:  optional
    	Directory where the files with the simulations results are
    	located. This path has to be relative to the root fdf.
    """
    _plot_type = 'Basis'

    _parameters = (

        SislObjectInput(key='geometry', name='Geometry',
            default=None,
            dtype=sisl.Geometry,
            help="""Geometry to take the basis orbitals from."""
        ),

        FloatInput(key='grid_prec', name='Grid precision',
            default=0.2,
            help="""The spacing between points of the grid where the basis will be projected (in Ang).
            If you are plotting a 3D representation, take into account that a very fine and big grid could result in
            your computer crashing on render. If it's the first time you are using this function,
            assess the capabilities of your computer by first using a low-precision grid and increase
            it gradually.
            """
        ),
        
        OrbitalQueries(
            key="orbitals", name="Orbitals",
            default=[],
            help="""Multiple queries to select the basis orbitals to be plotted.""",
            queryForm=[

                TextInput(
                    key="name", name="Name",
                    default="Orbital",
                    params={
                        "placeholder": "Name of the line..."
                    },
                ),

                'species', 'atoms', 'orbitals',

                ColorInput(
                    key="color", name="Color",
                    default=None,
                ),
                
                ColorInput(
                    key="neg_color", name="Negative color",
                    default=None
                ),
                
                FloatInput(
                    key="opacity", name="Opacity",
                    default=1,
                    
                )
            ]
        ),

    )

    _overwrite_defaults = {
        'axes': "xyz",
        'plot_geom': True
    }

    @entry_point('geometry', 0)
    def _read_from_geometry(self, geometry):
        """
        Plots the basis from anything that can be converted to a geometry.
        """
        self.geometry = sisl.Geometry.new(geometry)
        self.atoms = geometry.atoms

    def _after_read(self):
        # Just avoid here GridPlot's _after_grid. Note that we are
        # calling it later in _set_data
        self.get_param('orbitals').update_options(self.geometry)

    def _set_data(self, geometry, grid_prec, orbitals, nsc, axes, plot_geom):
        # Move all atoms inside the unit cell, otherwise the wavefunction is not
        # properly displayed.
        self.geometry = self.geometry.copy()
        self.geometry.xyz = (self.geometry.fxyz % 1).dot(self.geometry.cell)
        
        orb_param = self.get_param("orbitals")
        
        for_backend = []
        
        for i, orbital_group in enumerate(orbitals):
            
            orbital_group = orb_param.complete_query(orbital_group)

            orbs = orb_param.get_orbitals(orbital_group)
            
            if len(orbs) == 0:
                continue
        
            self.grid = sisl.Grid(grid_prec, geometry=self.geometry, dtype=np.float64)

            v = np.zeros(geometry.no)
            v[orbs] = 1
            
            sisl.physics.electron.wavefunction(v, self.grid, self.geometry)
            
            if np.any(self.grid.grid < 0):
                isos = [
                    {"val": -0.01}, {"val": 0.01, "color": orbital_group["neg_color"] or orbital_group["color"], "name": f'{orbital_group["name"]}, neg'}
                ]
            else:
                isos=[{"frac": 0.01}]
                
            isos = [
                {"color": orbital_group["color"], "name": orbital_group["name"], "opacity": orbital_group["opacity"], **iso} 
                for iso in isos
            ]
            
            for_backend.append(super()._set_data(trace_name=orbital_group["name"], isos=isos, plot_geom=plot_geom and i == 0))                
    
        return for_backend
    
    def split_groups(self, on="orbitals", only=None, exclude=None, clean=True, colors=(), **kwargs):
        """
        Builds groups automatically to draw their contributions.
        Works exactly the same as `Fatbands.split_groups`
        Parameters
        --------
        on: str, {"species", "atoms", "Z", "orbitals", "n", "l", "m", "zeta", "spin"} or list of str
            the parameter to split along.
            Note that you can combine parameters with a "+" to split along multiple parameters
            at the same time. You can get the same effect also by passing a list.
        only: array-like, optional
            if desired, the only values that should be plotted out of
            all of the values that come from the splitting.
        exclude: array-like, optional
            values that should not be plotted
        clean: boolean, optional
            whether the plot should be cleaned before drawing.
            If False, all the groups that come from the method will
            be drawn on top of what is already there.
        colors: array-like, optional
            A list of colors to be used. There can be more colors than
            needed, or less. If there are less colors than groups, the colors
            will just be repeated.
        **kwargs:
            keyword arguments that go directly to each request.
            This is useful to add extra filters. For example:
            `plot.split_groups(on="orbitals", species=["C"])`
            will split the PDOS on the different orbitals but will take
            only those that belong to carbon atoms.
        Examples
        -----------
        >>> plot = H.plot.fatbands()
        >>>
        >>> # Split the fatbands in n and l but show only the fatbands from Au
        >>> # Also use "Au $ns" as a template for the name, where $n will
        >>> # be replaced by the value of n.
        >>> plot.split_groups(on="n+l", species=["Au"], name="Au $ns")
        """
        groups = self.get_param('orbitals')._generate_queries(
            on=on, only=only, exclude=exclude, **kwargs)

        if len(colors) > 0:
            # Repeat the colors in case there are more groups than colors
            colors = np.tile(colors, len(groups) // len(colors) + 1)

            # Asign colors
            for i, _ in enumerate(groups):
                groups[i]['color'] = colors[i]

        # If the user doesn't want to clean the plot, we will just add the groups to the existing ones
        if not clean:
            groups = [*self.get_setting("orbitals"), *groups]

        return self.update_settings(orbitals=groups)