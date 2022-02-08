from .grid import PlotlyGridBackend
from ...templates import BasisBackend

from ....plots import BasisPlot

class PlotlyBasisBackend(BasisBackend, PlotlyGridBackend):
    pass

BasisPlot.backends.register("plotly", PlotlyBasisBackend)