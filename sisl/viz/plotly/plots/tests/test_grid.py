"""

Tests specific functionality of the grid plot.

Different inputs are tested (siesta .RHO and sisl Hamiltonian).

"""

import numpy as np
import os
import plotly.graph_objs as go

import sisl
from sisl.viz import GridPlot
from sisl.viz import Animation
from sisl.viz.plotly.plots.tests.get_files import from_files

# ------------------------------------------------------------
#         Build a generic tester for the bands plot
# ------------------------------------------------------------


class GridPlotTester:

    plot = None
    grid_shape = []

    def test_plotting_modes(self):

        plot = self.plot

        plot.update_settings(axes=[0])
        assert isinstance(plot.data[0], go.Scatter), "Not displaying grid in 1D correctly?"

        plot.update_settings(axes=[0, 1])
        assert isinstance(plot.data[0], go.Heatmap), "Not displaying grid in 2D correctly?"

        plot.update_settings(axes=[0, 1, 2], type3D="isosurface")
        assert isinstance(plot.data[0], go.Isosurface)

        plot.update_settings(type3D="volume")
        assert isinstance(plot.data[0], go.Volume)

    def test_grid(self):

        assert os.path.exists(self.plot.setting("grid_file")), "You provided a non-existent grid_file"

        grid = self.plot.grid

        assert isinstance(grid, sisl.Grid)
        assert grid.shape == self.grid_shape

    def test_scan(self):

        # AS_IS SCAN
        # Provide number of steps
        scanned = self.plot.scan(steps=2, mode="as_is")
        assert isinstance(scanned, Animation)
        assert len(scanned.frames) == 2

        # Provide step in Ang
        step = self.plot.grid.cell[0, 0]/2
        scanned = self.plot.scan(along=0, steps=step, mode="as_is")
        assert len(scanned.frames) == 2

        # Provide breakpoints
        breakpoints = [self.plot.grid.cell[0, 0]*frac for frac in [1/3, 2/3, 3/3]]
        scanned = self.plot.scan(along=0, breakpoints=breakpoints, mode="as_is")
        assert len(scanned.frames) == 2

        # 3D SCAN
        scanned = self.plot.scan(0, mode="moving_slice", breakpoints=breakpoints)

        assert isinstance(scanned, go.Figure)
        assert len(scanned.frames) == 3 # One cross section for each breakpoint

    def test_supercell(self):

        plot = self.plot

        plot.update_settings(axes=[0,1], interp=[1,1,1], sc=[1,1,1])

        # Check that the initial shapes are right
        prev_shape = (len(plot.data[0].x), len(plot.data[0].y))
        assert prev_shape == (plot.grid.shape[0], plot.grid.shape[1])

        # Check that the supercell is displayed
        plot.update_settings(sc=[2,1,1])
        sc_shape = (len(plot.data[0].x), len(plot.data[0].y))
        assert sc_shape[0] == 2*prev_shape[0]
        assert sc_shape[1] == prev_shape[1]

        plot.update_settings(sc=[1,1,1])

    def test_transforms(self):

        plot = self.plot

        plot.update_settings(axes=[0], transforms=["cos"])

        # Check that transforms = ["cos"] applies np.cos
        assert np.allclose(plot.data[0].y, np.cos(plot.grid.grid).mean(2).mean(1))
        


# ------------------------------------------------------------
#       Test the grid plot reading from siesta .RHO
# ------------------------------------------------------------

grid_file = from_files("SrTiO3.RHO")


class TestGridSiestaOutput(GridPlotTester):

    plot = GridPlot(grid_file=grid_file)
    grid_shape = (48, 48, 48)